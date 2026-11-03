# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

from MeowMusic import app
from MeowMusic.utils.database import is_command_locked

SPAM_CHATS = []


@app.on_message(
    filters.command(["report", "admin"], prefixes=["/", ".", "@", "!"]) & filters.group
)
async def report_admins(_, message):

    if await is_command_locked(message.chat.id, "report"):
        return

    replied = message.reply_to_message
    report_text = "`Reported to admins.`"

    if len(message.command) > 1:
        report_text = "`Reported to admins.`"

    SPAM_CHATS.append(message.chat.id)
    user_mentions = ""

    async for m in app.get_chat_members(message.chat.id):
        if message.chat.id not in SPAM_CHATS:
            break
        if m.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            user_mentions += f"[\u2063](tg://user?id={m.user.id})"

    if replied:
        await replied.reply_text(
            f"{report_text} {user_mentions}", disable_web_page_preview=True
        )
    else:
        await message.reply_text(
            f"{report_text} {user_mentions}", disable_web_page_preview=True
        )

    try:
        SPAM_CHATS.remove(message.chat.id)
    except Exception:
        pass
