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

JOKE_API_ENDPOINT = (
    "https://hindi-jokes-api.onrender.com/jokes?api_key=1a6d440e3f5971eecebceee818c2"
)


@app.on_message(filters.command("hjoke"))
async def joke(_, message):
    response = requests.get(JOKE_API_ENDPOINT)
    r = response.json()
    joke_text = r["jokeContent"]
    await message.reply_text(joke_text)
