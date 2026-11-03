# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters

from config import OWNER_ID
from MeowMusic import app


@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(_, message):

    if message.reply_to_message:

        destination_group_id = -1004454485434

        await message.reply_to_message.copy(destination_group_id)
        await message.reply("ᴘᴏsᴛ sᴜᴄᴄᴇssғᴜʟ ᴅᴏɴᴇ ")


@app.on_message(
    filters.command(["cpost"], prefixes=["/", "."]) & filters.user(OWNER_ID)
)
async def copy_messages(_, message):

    if message.reply_to_message:

        destination_group_id = -1004454485434

        await message.reply_to_message.copy(destination_group_id)
        await message.reply("Cʜᴀɴɴᴇʟ ᴘᴏsᴛ sᴜᴄᴄᴇssғᴜʟ ᴅᴏɴᴇ !")
