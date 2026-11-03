# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from inspect import getfullargspec
from io import BytesIO

import aiohttp
from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MeowMusic import app

button = InlineKeyboardMarkup(
    [[InlineKeyboardButton("⌯ ᴄʟᴏsᴇ ⌯", callback_data="close_data")]]
)


aiohttpsession = ClientSession()


async def post(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data


async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    try:
        screenshot_url = f"https://image.thum.io/get/fullpage/{url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(screenshot_url) as response:
                if response.status != 200:
                    return None
                image_bytes = await response.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

    file = BytesIO(image_bytes)
    file.name = "webss.jpg"
    return file


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(filters.command(["webss", "ss", "webshot"]) & filters.private)
async def take_ss(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="**ɢɪᴠᴇ ᴀ ᴜʀʟ ᴛᴏ ғᴇᴛᴄʜ sᴄʀᴇᴇɴsʜᴏᴛ.**")

    if len(message.command) == 2:
        url = message.text.split(None, 1)[1]
        full = False
    elif len(message.command) == 3:
        url = message.text.split(None, 2)[1]
        full = message.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
    else:
        return await eor(message, text="**ɪɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ.**")

    m = await eor(message, text="**ᴄᴀᴘᴛᴜʀɪɴɢ sᴄʀᴇᴇɴsʜᴏᴛ...**")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("**ғᴀɪʟᴇᴅ ᴛᴏ ᴛᴀᴋᴇ sᴄʀᴇᴇɴsʜᴏᴛ.**")

        m = await m.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ...**")

        if not full:
            await message.reply_photo(photo, reply_markup=button)
        else:
            await message.reply_photo(photo, reply_markup=button)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))
