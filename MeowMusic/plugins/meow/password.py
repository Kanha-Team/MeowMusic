# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MeowMusic import app


@app.on_message(filters.command(["genpassword", "genpw"]))
async def password(bot, update):
    message = await update.reply_text(text="Pʀᴏᴄᴇꜱꜱɪɴɢ..")
    password = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    if len(update.command) > 1:
        qw = update.text.split(" ", 1)[1]
    else:
        ST = ["5", "7", "6", "9", "10", "12", "14", "8", "13"]
        qw = random.choice(ST)
    limit = int(qw)
    random_value = "".join(random.sample(password, limit))
    txt = f"<b>Lɪᴍɪᴛ:</b> {limit!s} \n<b>Pᴀꜱꜱᴡᴏʀᴅ: <code>{random_value}</code>"
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "𝐀‌ᴅᴅ 𝐌‌є", url="https://t.me/MeowClonerBot?startgroup=true"
                )
            ]
        ]
    )
    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
