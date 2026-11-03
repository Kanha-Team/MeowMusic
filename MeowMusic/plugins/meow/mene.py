# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import requests
from pyrogram import filters

from MeowMusic import app

# Define a command handler for the /meme command


@app.on_message(filters.command("meme"))
async def meme_command(client, message):
    args = message.text.split()
    category = args[1] if len(args) > 1 else ""

    api_url = (
        f"https://meme-api.com/gimme/{category}"
        if category
        else "https://meme-api.com/gimme"
    )

    try:
        response = requests.get(api_url)
        data = response.json()

        if (
            response.status_code == 403
            or "message" in data
            and "Unable to Access Subreddit" in data["message"]
        ):
            await message.reply_text(
                "❌ Memes from this category are not found. Please try a different one."
            )
            return

        meme_url = data.get("url")
        title = data.get("title")

        bot_info = await app.get_me()

        caption = (
            f"{title}\n\n"
            f"Request by {message.from_user.mention}\n"
            f"Bot username: @{bot_info.username}"
        )

        await message.reply_photo(photo=meme_url, caption=caption)

    except Exception as e:
        print(f"Error fetching meme: {e}")
        await message.reply_text("Sorry, I couldn't fetch a meme at the moment.")
