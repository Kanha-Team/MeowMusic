# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MeowMusic import app
from MeowMusic.utils.decorators.language import language

C_BOT_USERNAME = "MeowClonerBot"

APP_LINK = f"https://t.me/{C_BOT_USERNAME}"

STREAMI_PICS = [
    "https://yukiapi.site/file/Ph2EelCC",
    "https://yukiapi.site/file/Ph2EelCC",
]

N_CLONE_MSG = f"Tᴏ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ᴄʟᴏɴᴇ, ᴜsᴇ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ʙᴏᴛ @{C_BOT_USERNAME}. Sɪᴍᴘʟʏ ɢᴏ ᴛʜᴇʀᴇ ᴀɴᴅ sᴛᴀʀᴛ ᴄʟᴏɴɪɴɢ!"


@app.on_message(filters.command("clone"))
@language
async def ping_clone(app: Client, message: Message, _):

    await message.reply_photo(
        photo=random.choice(STREAMI_PICS),
        caption=N_CLONE_MSG,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏɴᴇ Bᴏᴛ", url=APP_LINK)]]
        ),
    )
