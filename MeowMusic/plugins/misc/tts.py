# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from gtts import gTTS
from pyrogram import filters

from MeowMusic import app


@app.on_message(filters.command("tts"))
def text_to_speech(client, message):
    text = message.text.split(" ", 1)[1]
    tts = gTTS(text=text, lang="hi")
    tts.save("speech.mp3")
    client.send_audio(message.chat.id, "speech.mp3")
