# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters

from config import BOT_USERNAME
from MeowMusic import app


def hex_to_text(hex_string):
    try:
        text = bytes.fromhex(hex_string).decode("utf-8")
        return text
    except Exception as e:
        return f"Error decoding hex: {e!s}"


def text_to_hex(text):
    hex_representation = " ".join(format(ord(char), "x") for char in text)
    return hex_representation


# YOUR_ALPHA_BABY ...........................


@app.on_message(filters.command("code"))
def convert_text(_, message):
    if len(message.command) > 1:
        input_text = " ".join(message.command[1:])

        hex_representation = text_to_hex(input_text)
        decoded_text = hex_to_text(input_text)

        response_text = f"𝗜𝗻𝗽𝘂𝘁 𝗧𝗲𝘅𝘁➪\n {input_text}\n\n𝗛𝗲𝘅 𝗥𝗲𝗽𝗿𝗲𝘀𝗲𝗻𝘁𝗮𝘁𝗶𝗼𝗻➪\n {hex_representation}\n\n𝗗𝗲𝗰𝗼𝗱𝗲𝗱 𝗧𝗲𝘅𝘁➪\n {decoded_text}\n\n\n𝗕𝗬 ➪@{BOT_USERNAME}"

        message.reply_text(response_text)
    else:
        message.reply_text("Please provide text after the /code command.")
