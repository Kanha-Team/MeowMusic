# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MeowMusic import app
from MeowMusic.plugins.tools.pretenderdb import (
    add_userdata,
    check_pretender,
    get_userdata,
    impo_off,
    impo_on,
    usr_data,
)

MEOW = [
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/84e84ff778b045879d24f.jpg",
    "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/d6360613d0fa7a9d2f90b.jpg",
    "https://graph.org/file/37248e7bdff70c662a702.jpg",
    "https://graph.org/file/0bfe29d15e918917d1305.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/e6b01f23f2871e128dad8.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
    "https://graph.org/file/ddc5d6ec1c33276507b19.jpg",
    "https://graph.org/file/39d7277189360d2c85b62.jpg",
    "https://graph.org/file/5846b9214eaf12c3ed100.jpg",
    "https://graph.org/file/ad4f9beb4d526e6615e18.jpg",
    "https://graph.org/file/3514efaabe774e4f181f2.jpg",
]


KANHA = [
    [
        InlineKeyboardButton(
            text="ᴀᴅᴅ ᴍᴇ", url="https://t.me/MeowClonerBot?startgroup=true"
        ),
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url="https://t.me/MeowCloner"),
    ],
]


@app.on_message(filters.group & ~filters.bot & ~filters.via_bot, group=69)
async def chk_usr(_, message: Message):
    if message.sender_chat or not await check_pretender(message.chat.id):
        return
    if not await usr_data(message.from_user.id):
        return await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    usernamebefore, first_name, lastname_before = await get_userdata(
        message.from_user.id
    )
    msg = ""
    if (
        usernamebefore != message.from_user.username
        or first_name != message.from_user.first_name
        or lastname_before != message.from_user.last_name
    ):
        msg += f"""
**♥︎ ᴜsᴇʀ sʜᴏʀᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ♥︎**

**๏ ɴᴀᴍᴇ** ➛ {message.from_user.mention}
**๏ ᴜsᴇʀ ɪᴅ** ➛ {message.from_user.id}
"""
    if usernamebefore != message.from_user.username:
        usernamebefore = f"@{usernamebefore}" if usernamebefore else "NO USERNAME"
        usernameafter = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else "NO USERNAME"
        )
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇᴅ ᴜsᴇʀɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {usernamebefore}
**๏ ᴀғᴛᴇʀ** ➛ {usernameafter}
"""
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if first_name != message.from_user.first_name:
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇs ғɪʀsᴛ ɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {first_name}
**๏ ᴀғᴛᴇʀ** ➛ {message.from_user.first_name}
"""
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if lastname_before != message.from_user.last_name:
        lastname_before = lastname_before or "NO LAST NAME"
        lastname_after = message.from_user.last_name or "NO LAST NAME"
        msg += f"""
**♥︎ ᴄʜᴀɴɢᴇs ʟᴀsᴛ ɴᴀᴍᴇ ♥︎**

**๏ ʙᴇғᴏʀᴇ** ➛ {lastname_before}
**๏ ᴀғᴛᴇʀ** ➛ {lastname_after}
"""
        await add_userdata(
            message.from_user.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name,
        )
    if msg != "":
        await message.reply_photo(
            random.choice(MEOW),
            caption=msg,
            reply_markup=InlineKeyboardMarkup(KANHA),
        )


@app.on_message(
    filters.group & filters.command("imposter") & ~filters.bot & ~filters.via_bot
)
async def set_mataa(_, message: Message):
    usage = "**ᴅᴇᴛᴇᴄᴛ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴜsᴇʀs ᴜsᴀɢᴇ : /imposter ᴏɴ|ᴏғғ**"
    if len(message.command) < 2:
        return await message.reply(usage)

    arg = message.command[1].lower()
    if arg in ("on", "enable"):
        was_on = await impo_on(message.chat.id)
        if was_on:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
        else:
            await message.reply(
                f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴇɴᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}"
            )
    elif arg in ("off", "disable"):
        was_on = await impo_off(message.chat.id)
        if not was_on:
            await message.reply("**ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
        else:
            await message.reply(
                f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴅɪsᴀʙʟᴇᴅ ᴘʀᴇᴛᴇɴᴅᴇʀ ᴍᴏᴅᴇ ғᴏʀ** {message.chat.title}"
            )
    else:
        await message.reply(usage)
