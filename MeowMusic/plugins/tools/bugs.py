# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import html
import logging
import time

from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import BANNED_USERS, LOGGER_ID, OWNER_ID
from MeowMusic import app

BUG_COOLDOWN = 5 * 60
_last_report: dict[tuple, float] = {}


def _flood_remaining(key: tuple) -> float:
    last = _last_report.get(key)
    if last is None:
        return 0
    remaining = BUG_COOLDOWN - (time.time() - last)
    return max(0, remaining)


def _format_minutes(seconds: float) -> str:
    minutes = max(1, int(seconds // 60) + (1 if seconds % 60 else 0))
    return f"{minutes} minute"


@app.on_message(filters.command("bug") & ~BANNED_USERS)
async def bug_report(client, message: Message):
    if message.from_user is None:
        return

    parts = message.text.split(None, 1)
    reason = parts[1].strip() if len(parts) > 1 else ""
    replied = message.reply_to_message

    if not reason and replied is None:
        return await message.reply_text(
            "<b>Usage:</b> <code>/bug &lt;description&gt;</code> or reply to a message with <code>/bug</code>.",
            parse_mode=ParseMode.HTML,
        )

    flood_key = (client.me.id, message.chat.id, message.from_user.id)
    remaining = _flood_remaining(flood_key)
    if remaining > 0:
        return await message.reply_text(
            f"<b>You can report once every 5 minutes. Try again in {_format_minutes(remaining)}.</b>",
            parse_mode=ParseMode.HTML,
        )
    _last_report[flood_key] = time.time()

    targets = {chat_id for chat_id in (LOGGER_ID, OWNER_ID) if chat_id}

    if replied is not None:
        for chat_id in targets:
            try:
                await replied.forward(chat_id)
            except Exception as e:
                logging.warning(f"bug: forward to {chat_id} failed: {e}")

    user = message.from_user
    mention = (
        f'<a href="tg://user?id={user.id}">{html.escape(user.first_name or "user")}</a>'
    )

    if message.chat.type.name == "PRIVATE":
        chat_name = "Private chat"
    else:
        chat_name = html.escape(message.chat.title or "group")
        if message.chat.username:
            chat_name = (
                f'<a href="https://t.me/{message.chat.username}">{chat_name}</a>'
            )

    report_text = html.escape(reason) if reason else "Reply only (no text)"
    report = (
        "<b>#BUG</b>\n\n"
        f"<b>Reported by:</b> {mention}\n"
        f"<b>User ID:</b> <code>{user.id}</code>\n"
        f"<b>Chat:</b> {chat_name} | <code>{message.chat.id}</code>\n\n"
        f"<b>Bug:</b> {report_text}"
    )

    rows = []
    if message.link:
        rows.append([InlineKeyboardButton("⌯ View Bug ⌯", url=message.link)])
    rows.append([InlineKeyboardButton("⌯ Close ⌯", callback_data="bug_close")])
    report_markup = InlineKeyboardMarkup(rows)

    for chat_id in targets:
        try:
            await client.send_message(
                chat_id,
                report,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
                reply_markup=report_markup,
            )
        except Exception as e:
            logging.warning(f"bug: send report to {chat_id} failed: {e}")

    await message.reply_text(
        "<b>Bug report sent! Our developers will look into it soon.</b>",
        parse_mode=ParseMode.HTML,
    )


@app.on_callback_query(filters.regex("^bug_close$"))
async def bug_close(client, query: CallbackQuery):
    try:
        member = await client.get_chat_member(query.message.chat.id, query.from_user.id)
        can_delete = bool(member.privileges and member.privileges.can_delete_messages)
    except Exception:
        can_delete = False

    if not can_delete:
        return await query.answer(
            "You do not have permission to close this.", show_alert=True
        )
    await query.message.delete()
