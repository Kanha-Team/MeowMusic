# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import io

import qrcode
from pyrogram import filters
from pyrogram.types import Message

from MeowMusic import app


# Function to create a QR code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="white", back_color="black")

    # Save the QR code to a bytes object to send with Pyrogram
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)  # Go to the start of the bytes object

    return img_bytes


@app.on_message(filters.command("qr"))
def qr_handler(client, message: Message):
    # Extracting the text passed after the command
    command_text = message.command
    if len(command_text) > 1:
        input_text = " ".join(command_text[1:])
        qr_image = generate_qr_code(input_text)
        message.reply_photo(qr_image, caption="Here's your QR Code")
    else:
        message.reply_text(
            "Please provide the text for the QR code after the command. Example usage: /qr text"
        )
