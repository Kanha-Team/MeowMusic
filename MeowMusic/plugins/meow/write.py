# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from datetime import datetime

import requests
from pyrogram import *
from pyrogram import filters
from pyrogram.types import Message

from config import BOT_USERNAME
from MeowMusic import app


@app.on_message(filters.command("write"))
async def handwrite(_, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = message.text.split(None, 1)[1]
    m = await message.reply_text("Please wait...,\n\nWriting your text...")
    write = requests.get(f"https://apis.xditya.me/write?text={text}").url

    caption = f"""
sᴜᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ 💘
✨ ᴡʀɪᴛᴛᴇɴ ʙʏ : [𝐘ᴜᴍɪᴋᴏᴏ](https://t.me/{BOT_USERNAME})
🥀 ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ : {message.from_user.mention}
"""
    await m.delete()
    await message.reply_photo(photo=write, caption=caption)


mod_name = "WʀɪᴛᴇTᴏᴏʟ"

help = """

 ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴡʜɪᴛᴇ ᴘᴀɢᴇ ᴡɪᴛʜ ᴀ ᴘᴇɴ 🖊

❍ /write <ᴛᴇxᴛ> *:* ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.
 """


# ----------


@app.on_message(filters.command("day"))
def date_to_day_command(client: Client, message: Message):
    try:
        # Extract the date from the command message......
        command_parts = message.text.split(" ", 1)
        if len(command_parts) == 2:
            input_date = command_parts[1].strip()
            date_object = datetime.strptime(input_date, "%Y-%m-%d")
            day_of_week = date_object.strftime("%A")

            # Reply with the day of the week
            message.reply_text(
                f"The day of the week for {input_date} is {day_of_week}."
            )

        else:
            message.reply_text(
                "Please provide a valid date in the format `/day 1947-08-15` "
            )

    except ValueError as e:
        message.reply_text(f"Error: {e!s}")
