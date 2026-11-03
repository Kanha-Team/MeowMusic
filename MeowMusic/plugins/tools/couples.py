# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random
import re
import time

import aiohttp
from pyrogram import Client, enums, filters, types
from pyrogram.errors import FloodWait

from config import BANNED_USERS
from MeowMusic import app
from MeowMusic.core.userbot import assistantids
from MeowMusic.utils.meow_font import Fonts

COOLDOWN_SECONDS = 5 * 60

_last_used: dict[int, float] = {}
_current_couple: dict[int, tuple[types.User, types.User]] = {}

COUPLE_IMAGES: list[str] = [
    "https://d.uguu.se/ekaLoJcg.jpg",
    "https://h.uguu.se/mminlleb.jpg",
]

_NEKO_CATEGORIES = ["kiss", "hug", "cuddle"]


async def _fetch_image_url() -> str | None:
    if COUPLE_IMAGES:
        return random.choice(COUPLE_IMAGES)

    category = random.choice(_NEKO_CATEGORIES)
    headers = {"User-Agent": "MeowMusic/1.0 (https://github.com/Kanha-Team/MeowMusic)"}
    try:
        async with (
            aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session,
            session.get(
                f"https://nekos.best/api/v2/{category}", headers=headers
            ) as resp,
        ):
            if resp.status == 200 and "application/json" in (
                resp.headers.get("Content-Type") or ""
            ):
                data = await resp.json()
                results = data.get("results") or []
                if results and results[0].get("url"):
                    return results[0]["url"]
    except Exception as e:
        print(f"[COUPLE] nekos.best fetch failed: {e}")

    return f"https://picsum.photos/800/600?random={random.randint(1, 1_000_000)}"


def font(text: str) -> str:
    if not text:
        return ""

    segments = re.split(r"(<[^>]+>)", text)
    styled_segments = []
    for segment in segments:
        if segment.startswith("<") and segment.endswith(">"):
            styled_segments.append(segment)
        else:
            styled_text = ""
            for char in segment:
                try:
                    if char.isupper():
                        styled_text += Fonts.serief(char)
                    elif char.islower():
                        styled_text += Fonts.smallcap(char)
                    else:
                        styled_text += char
                except Exception:
                    styled_text += char
            styled_segments.append(styled_text)

    return "".join(styled_segments)


def _mention(user: types.User) -> str:
    return f"@{user.username}" if user.username else user.mention


async def _pick_two_members(c: Client, chat_id: int) -> list[types.User] | None:
    assistant_ids = set(assistantids)
    candidates = []
    try:
        async for member in c.get_chat_members(chat_id, limit=200):
            u = member.user
            if u and not u.is_bot and not u.is_deleted and u.id not in assistant_ids:
                candidates.append(u)
    except Exception:
        return None

    if len(candidates) < 2:
        return None

    return random.sample(candidates, 2)


@app.on_message(filters.command(["couple"]) & filters.group & ~BANNED_USERS)
async def couple_of_the_day(c: Client, message: types.Message):
    chat_id = message.chat.id
    now = time.time()

    last = _last_used.get(chat_id)
    if last and (now - last) < COOLDOWN_SECONDS:
        remaining = int(COOLDOWN_SECONDS - (now - last))
        mins, secs = divmod(remaining, 60)
        return await message.reply_text(
            font(
                f"⏳ A couple has been declared recently.\nTry again in {mins}m {secs}s."
            )
        )

    pair = await _pick_two_members(c, chat_id)
    if not pair:
        return await message.reply_text(
            font("❌ Not enough members here to pick a couple!")
        )

    _last_used[chat_id] = now

    user1, user2 = pair
    _current_couple[chat_id] = (user1, user2)
    bot_name = c.me.first_name if c.me else "Bot"
    caption = (
        f"❤️ <b>{font('Todays Husband and Wife')}</b> ❤️\n\n"
        f"👨 {font('Husband')}: {_mention(user1)}\n"
        f"👩 {font('Wife')}: {_mention(user2)}\n\n"
        f"{font('Made for each other')} 💞\n\n"
        f"~ {font(f'From {bot_name} with love')} 💋"
    )

    image = await _fetch_image_url()

    try:
        if image:
            await message.reply_photo(
                image, caption=caption, parse_mode=enums.ParseMode.HTML
            )
        else:
            await message.reply_text(
                caption, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
            )
    except FloodWait:
        raise
    except Exception:
        try:
            await message.reply_text(
                caption, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
            )
        except Exception:
            pass


@app.on_message(filters.command(["divorce"]) & filters.group & ~BANNED_USERS)
async def divorce_couple(c: Client, message: types.Message):
    chat_id = message.chat.id

    couple = _current_couple.get(chat_id)
    if not couple:
        return await message.reply_text(
            font("❌ No couple has been assigned in this group yet. Use /couple first.")
        )

    user1, user2 = couple

    _current_couple.pop(chat_id, None)
    _last_used.pop(chat_id, None)

    caption = (
        f"💔 <b>{font('Divorce Announced')}</b> 💔\n\n"
        f"👨 {font('Husband')}: {_mention(user1)}\n"
        f"👩 {font('Wife')}: {_mention(user2)}\n\n"
        f"{font('Their marriage has officially ended')} 😢\n\n"
        f"~ {font('Use /couple to find new love')} 💘"
    )

    await message.reply_text(
        caption, parse_mode=enums.ParseMode.HTML, disable_web_page_preview=True
    )
