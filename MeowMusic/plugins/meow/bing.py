# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import requests as r
from pyrogram import filters

from MeowMusic import app

API_URL = "https://sugoi-api.vercel.app/search"


@app.on_message(filters.command("bingsearch"))
async def bing_search(michiko, message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(
            message.command[1:]
        )  # Assuming the keyword is passed as arguments
        params = {"keyword": keyword}
        response = r.get(API_URL, params=params)

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("\x74\x69\x74\x6c\x65", "")
                    link = result.get("\x6c\x69\x6e\x6b", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e!s}")
