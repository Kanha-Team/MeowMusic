# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random
from os import getenv

import aiohttp
from pyrogram import filters
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BANNED_USERS
from MeowMusic import app
from MeowMusic.core.mongo import mongodb

OPENROUTER_API_KEY = getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

chatbot_settings = mongodb.chatbot_settings

SYSTEM_PROMPT = (
    "You are Meow, a friendly assistant in a Telegram chat. "
    "Reply in Hinglish (Hindi written in English letters), like a normal chat message. "
    "Keep replies short: one or two sentences. "
    "Be warm and helpful, use at most one emoji, and do not use romantic or possessive roleplay. "
    "Do not guilt-trip or sulk if someone ignores you. "
    "Never say you are a human, and never claim to have feelings in a way meant to create emotional dependence."
)

ERROR_MESSAGES = [
    "Abhi thodi busy hoon, thodi der mein try karo.",
    "Signal weak hai, baad mein baat karte hain.",
    "Ek second, abhi reply nahi de pa rahi.",
]

_chat_cache: dict[int, bool] = {}
_global_enabled = True


def get_send_status() -> bool:
    return _global_enabled


async def is_chatbot_enabled(chat_id: int) -> bool:
    if chat_id in _chat_cache:
        return _chat_cache[chat_id]
    doc = await chatbot_settings.find_one({"chat_id": chat_id})
    enabled = doc is None
    _chat_cache[chat_id] = enabled
    return enabled


async def set_chatbot_enabled(chat_id: int, enabled: bool) -> None:
    if enabled:
        await chatbot_settings.delete_one({"chat_id": chat_id})
    else:
        await chatbot_settings.update_one(
            {"chat_id": chat_id}, {"$set": {"chat_id": chat_id}}, upsert=True
        )
    _chat_cache[chat_id] = enabled


async def ask_question(message: str) -> str:
    if not OPENROUTER_API_KEY:
        return random.choice(ERROR_MESSAGES)

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        "temperature": 0.9,
        "max_tokens": 80,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Kanha-Team/MeowMusic",
        "X-Title": "MeowMusic",
    }
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                OPENROUTER_URL, json=payload, headers=headers
            ) as resp:
                if resp.status != 200:
                    return random.choice(ERROR_MESSAGES)
                data = await resp.json()
                reply = data["choices"][0]["message"]["content"] or ""
                reply = reply.strip()
                return reply or random.choice(ERROR_MESSAGES)
    except (TimeoutError, aiohttp.ClientError, KeyError, ValueError):
        return random.choice(ERROR_MESSAGES)


async def _is_admin(client, message_or_query) -> bool:
    if isinstance(message_or_query, CallbackQuery):
        chat_id = message_or_query.message.chat.id
        user_id = message_or_query.from_user.id
    else:
        chat_id = message_or_query.chat.id
        user_id = message_or_query.from_user.id
    try:
        member = await client.get_chat_member(chat_id, user_id)
    except Exception:
        return False
    return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)


text_filter = filters.text & ~filters.bot & ~filters.regex(r"^[/!.#]")


@app.on_message(filters.command("chatbot") & filters.group & ~BANNED_USERS)
async def chatbot_toggle(client, message: Message):
    if not await _is_admin(client, message):
        return

    enabled = await is_chatbot_enabled(message.chat.id)
    status_text = "ᴇɴᴀʙʟᴇᴅ" if enabled else "ᴅɪꜱᴀʙʟᴇᴅ"

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴇɴᴀʙʟᴇ", callback_data="chatbot_enable"),
                InlineKeyboardButton("ᴅɪꜱᴀʙʟᴇ", callback_data="chatbot_disable"),
            ]
        ]
    )
    await message.reply_text(
        f"❖ ᴄᴜʀʀᴇɴᴛʟʏ ᴄʜᴀᴛʙᴏᴛ ɪꜱ **{status_text}** ɪɴ **{message.chat.title}**.",
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("^chatbot_(enable|disable)$") & ~BANNED_USERS)
async def chatbot_toggle_button(client, query: CallbackQuery):
    if not await _is_admin(client, query):
        return await query.answer("ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs.", show_alert=True)

    chat_id = query.message.chat.id
    enabling = query.data == "chatbot_enable"
    currently = await is_chatbot_enabled(chat_id)

    if enabling and currently:
        return await query.answer("ᴄʜᴀᴛʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.", show_alert=True)
    if not enabling and not currently:
        return await query.answer("ᴄʜᴀᴛʙᴏᴛ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴅɪꜱᴀʙʟᴇᴅ.", show_alert=True)

    await set_chatbot_enabled(chat_id, enabling)
    state = "ᴇɴᴀʙʟᴇᴅ" if enabling else "ᴅɪꜱᴀʙʟᴇᴅ"
    await query.message.edit_text(
        f"❖ ᴄʜᴀᴛʙᴏᴛ ʜᴀꜱ ʙᴇᴇɴ **{state}** ʙʏ {query.from_user.mention}."
    )
    await query.answer(f"ᴄʜᴀᴛʙᴏᴛ {state} !!")


@app.on_message(filters.group & text_filter & ~BANNED_USERS)
async def group_chatbot(client, message: Message):
    if len(message.text) > 69:
        return
    if not await is_chatbot_enabled(message.chat.id):
        return

    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    reply = await ask_question(message.text)
    await message.reply_text(reply)


@app.on_message(filters.private & text_filter & ~BANNED_USERS)
async def private_chatbot(client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    reply = await ask_question(message.text)
    await message.reply_text(reply)
