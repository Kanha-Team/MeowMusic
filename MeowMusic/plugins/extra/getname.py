# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import base64

import aiohttp
from pyrogram import Client, filters
from pyrogram.types import Message

from config import OWNER_ID
from MeowMusic import app

API_TOKEN = "USER-TOKEN-7355202884"
API_URL = "https://aizensolo.ru/search/media"


@app.on_message(
    filters.command(["waifu"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
)
async def get_character_name(client: Client, message: Message):
    reply = message.reply_to_message

    if not reply:
        await message.reply("__please reply to a photo__")
        return

    # auto detect bot id from spawn message
    if not reply.from_user or not reply.from_user.id:
        await message.reply("__please reply to a photo__")
        return

    bot_id = reply.from_user.id

    media_type = None
    file_bytes = None

    if reply.photo:
        media_type = "photo"
        file = await reply.download(in_memory=True)
        file_bytes = file.getbuffer()

    elif reply.video or reply.animation:
        media_type = "video"
        file = await reply.download(in_memory=True)
        file_bytes = file.getbuffer()

    else:
        await message.reply("__please reply to a photo__")
        return

    try:
        encoded_string = base64.b64encode(file_bytes).decode()

        headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}

        data = {"media_type": media_type, "media": encoded_string, "bot_id": bot_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=data, headers=headers) as resp:

                if resp.status != 200:
                    await app.send_message(
                        chat_id=OWNER_ID, text="Waifu API returned status code."
                    )
                    return await message.reply(
                        "__API seems to be down or returned an error.__"
                    )

                result = await resp.json()

        # not found
        if result.get("status") == "not_found":
            return await message.reply("__Character not found in the database.__")

        # perfect / close
        if result.get("match_type") in ["perfect", "close"]:
            name = result.get("name", "Unknown")
            prefix = result.get("command", "").strip()
            first_name = name.split()[0]

            text = f"""**Name:** `{name}`

**Humanizer:** `{prefix} {first_name}`
**Command:** `{prefix} {name}`"""

            return await message.reply(text)

        # multiple matches
        if result.get("match_type") == "multiple":
            first = result.get("names", [])[0]
            name = first.get("name", "Unknown")
            prefix = first.get("command", "").strip()
            first_name = name.split()[0]

            text = f"""**Name:** `{name}`

**Humanizer:** `{prefix} {first_name}`
**Command:** `{prefix} {name}`"""

            return await message.reply(text)

        await message.reply("__sorry, I couldn't recognize the character.__")

    except Exception:
        await message.reply("Error occurred..")
