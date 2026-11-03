# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired

from MeowMusic import app
from MeowMusic.misc import SUDOERS


@app.on_message(filters.command("link") & SUDOERS)
async def link_handler(client, message):
    if len(message.command) < 2:
        return await message.reply_text("ᴘʀᴏᴠɪᴅᴇ ᴀ ᴄʜᴀᴛ ɪᴅ ᴛᴏ ʀᴇᴛʀɪᴇᴠᴇ ɪᴛs ʟɪɴᴋ.")

    target_chat_id = message.command[1]

    try:
        chat = await app.get_chat(int(target_chat_id))
        if chat.username:
            chat_link = f"https://t.me/{chat.username}"
        else:
            chat_link = await app.export_chat_invite_link(int(target_chat_id))

        await message.reply_text(f"ʜᴇʀᴇ ɪs ᴛʜᴇ ᴄʜᴀᴛ ʟɪɴᴋ ғᴏʀ {chat.title}: {chat_link}")

    except ChatAdminRequired:
        return await message.reply_text(
            "ɪ'ᴍ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ᴏʀ ɴᴏᴛ ᴛʜᴇʀᴇ."
        )
    except Exception as e:
        return await message.reply_text(
            f"An error occurred: {type(e).name}. Please try again later."
        )
