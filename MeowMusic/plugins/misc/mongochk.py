# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import re

from pymongo import MongoClient
from pymongo.errors import ConfigurationError, ServerSelectionTimeoutError
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from MeowMusic import app as Meow

# ✦ Mongo URL Regex
MONGO_URL_PATTERN = re.compile(r"^mongodb(\+srv)?:\/\/[^\s]+$")


# ✦ Add Bot Button
def add_me_button():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ 𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐆ʀᴏᴜᴘ ➕",
                    url=f"https://t.me/{Kanha.username}?startgroup=true",
                )
            ]
        ]
    )


# ============================= #
# 💾 𝐌ᴏɴɢᴏ 𝐂ʜᴇᴄᴋ 𝐂ᴏᴍᴍᴀɴᴅ
# ============================= #


@Meow.on_message(filters.command("mongochk"))
async def mongo_command(client, message: Message):

    # ❌ No URL Provided
    if len(message.command) < 2:
        return await message.reply_text(
            "╭━━━〔 💾 𝐌ᴏɴɢᴏ 𝐂ʜᴇᴄᴋᴇʀ 💾 〕━━━╮\n"
            "┃ ✘ 𝐏ʟᴇᴀsᴇ 𝐏ʀᴏᴠɪᴅᴇ 𝐌ᴏɴɢᴏ 𝐔𝐑𝐋\n"
            "┃ \n"
            "┃ ✎ 𝐄xᴀᴍᴘʟᴇ:\n"
            "┃ `/mongochk mongodb+srv://user:pass@cluster.mongodb.net/`\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )

    mongo_url = message.command[1].strip()

    # ❌ Invalid Format
    if not MONGO_URL_PATTERN.match(mongo_url):
        return await message.reply_text(
            "╭━━━〔 ⚠️ 𝐈ɴᴠᴀʟɪᴅ 𝐅ᴏʀᴍᴀᴛ ⚠️ 〕━━━╮\n"
            "┃ 💔 𝐖ʀᴏɴɢ 𝐌ᴏɴɢᴏ𝐃𝐁 𝐔𝐑𝐋\n"
            "┃ \n"
            "┃ ✔ 𝐒ʜᴏᴜʟᴅ 𝐒ᴛᴀʀᴛ 𝐖ɪᴛʜ:\n"
            "┃ ➜ mongodb://\n"
            "┃ ➜ mongodb+srv://\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )

    # 🔄 Checking Message
    checking_msg = await message.reply_text(
        "╭━━━〔 🔄 𝐏ʀᴏᴄᴇssɪɴɢ 🔄 〕━━━╮\n"
        "┃ ⏳ 𝐂ʜᴇᴄᴋɪɴɢ 𝐌ᴏɴɢᴏ𝐃𝐁 𝐂ᴏɴɴᴇᴄᴛɪᴏɴ...\n"
        "╰━━━━━━━━━━━━━━━━━━━━╯"
    )

    try:
        mongo_client = MongoClient(
            mongo_url, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000
        )

        mongo_client.server_info()

        await checking_msg.edit_text(
            "╭━━━〔 ✅ 𝐒ᴜᴄᴄᴇss ✅ 〕━━━╮\n"
            "┃ 🎉 𝐌ᴏɴɢᴏ𝐃𝐁 𝐂ᴏɴɴᴇᴄᴛᴇᴅ 𝐒ᴜᴄᴄᴇssғᴜʟʟʏ\n"
            "┃ \n"
            f"┃ 👤 𝐂ʜᴇᴄᴋᴇᴅ 𝐁ʏ: {message.from_user.mention}\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )

    except ServerSelectionTimeoutError:
        await checking_msg.edit_text(
            "╭━━━〔 ⏰ 𝐓ɪᴍᴇᴏᴜᴛ ⏰ 〕━━━╮\n"
            "┃ ❌ 𝐂ᴏɴɴᴇᴄᴛɪᴏɴ 𝐓ɪᴍᴇᴅ 𝐎ᴜᴛ\n"
            "┃ 🌐 𝐂ʜᴇᴄᴋ 𝐍ᴇᴛᴡᴏʀᴋ / 𝐂ʟᴜsᴛᴇʀ\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )

    except ConfigurationError:
        await checking_msg.edit_text(
            "╭━━━〔 ⚙️ 𝐂ᴏɴғɪɢ 𝐄ʀʀᴏʀ ⚙️ 〕━━━╮\n"
            "┃ ❌ 𝐈ɴᴠᴀʟɪᴅ 𝐔sᴇʀɴᴀᴍᴇ / 𝐏ᴀssᴡᴏʀᴅ\n"
            "┃ 🔐 𝐂ʜᴇᴄᴋ 𝐂ʟᴜsᴛᴇʀ 𝐒ᴇᴛᴛɪɴɢs\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )

    except Exception as e:
        await checking_msg.edit_text(
            "╭━━━〔 💥 𝐅ᴀɪʟᴇᴅ 💥 〕━━━╮\n"
            f"┃ ❌ 𝐄ʀʀᴏʀ: {e!s}\n"
            "╰━━━━━━━━━━━━━━━━━━━━╯",
            reply_markup=add_me_button(),
        )
