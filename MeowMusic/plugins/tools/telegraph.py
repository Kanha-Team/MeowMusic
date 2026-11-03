# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import html as html_lib
import json
import os

import aiohttp
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from MeowMusic import app

YUKI_UPLOAD_URL = "https://yukiapi.site/upload"
MAX_FILE_SIZE = 100 * 1024 * 1024
UPLOAD_TIMEOUT = 300

USAGE = (
    "<b>❖ Reply to a media file to upload it.</b>\n\n"
    "<blockquote>» Supported: photo, video, document, audio, voice\n» Max size: 100 MB</blockquote>"
)


def _media_info(msg: Message):
    if msg.photo:
        return "photo.jpg", msg.photo.file_size or 0
    if msg.video:
        return msg.video.file_name or "video.mp4", msg.video.file_size or 0
    if msg.document:
        return msg.document.file_name or "document", msg.document.file_size or 0
    if msg.audio:
        return msg.audio.file_name or "audio.mp3", msg.audio.file_size or 0
    if msg.voice:
        return "voice.ogg", msg.voice.file_size or 0
    return None


async def _upload_to_yuki(path: str, name: str) -> str:
    timeout = aiohttp.ClientTimeout(total=UPLOAD_TIMEOUT)
    with open(path, "rb") as f:
        form = aiohttp.FormData()
        form.add_field("file", f, filename=os.path.basename(name))
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(YUKI_UPLOAD_URL, data=form) as resp:
                body = (await resp.text()).strip()
                if not body:
                    raise RuntimeError("YukiAPI: empty response")
                if resp.status != 200:
                    raise RuntimeError(f"YukiAPI: {resp.status} - {body[:100]}")
                try:
                    url = json.loads(body).get("url", "")
                except (ValueError, AttributeError):
                    raise RuntimeError(f"YukiAPI: unexpected response - {body[:100]}")
                if not url.startswith("http"):
                    raise RuntimeError(f"YukiAPI: {body[:100]}")
                return url


def _format_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024:
            return f"{num:.2f} {unit}"
        num /= 1024
    return f"{num:.2f} TB"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]) & ~BANNED_USERS)
async def upload_media(client, message: Message):
    media_msg = message.reply_to_message
    if media_msg is None:
        return await message.reply_text(USAGE, parse_mode=ParseMode.HTML)

    info = _media_info(media_msg)
    if info is None:
        return await message.reply_text(
            "<b>⚠️ Unsupported media type.</b>", parse_mode=ParseMode.HTML
        )

    name, size = info
    if size > MAX_FILE_SIZE:
        return await message.reply_text(
            f"<b>⚠️ File too large!</b>\n<blockquote>Size: {_format_size(size)}\nMax: 100 MB</blockquote>",
            parse_mode=ParseMode.HTML,
        )

    status = await message.reply_text(
        "<b>⏳ Processing...</b>", parse_mode=ParseMode.HTML
    )
    path = None
    try:
        await status.edit_text("<b>📥 Downloading...</b>", parse_mode=ParseMode.HTML)
        path = await media_msg.download()
        if not path or not os.path.exists(path):
            raise RuntimeError("downloaded file missing")

        await status.edit_text(
            "<b>📤 Uploading via YukiAPI...</b>", parse_mode=ParseMode.HTML
        )
        link = await _upload_to_yuki(path, name)

        real_size = os.path.getsize(path)
        text = (
            "<b>Uploaded successfully!</b>\n\n"
            "<blockquote>"
            f"➤ <b>File:</b> <code>{html_lib.escape(name)}</code>\n"
            f"➤ <b>Size:</b> <code>{_format_size(real_size)}</code>\n"
            "➤ <b>Service:</b> <code>YukiAPI</code>"
            "</blockquote>\n\n"
            f"🔗 {html_lib.escape(link)}"
        )
        await status.edit_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("• YukiAPI Link •", url=link)]]
            ),
        )
    except Exception as e:
        await status.edit_text(
            f"<b>❌ Upload failed!</b>\n<blockquote>{html_lib.escape(str(e))}</blockquote>",
            parse_mode=ParseMode.HTML,
        )
    finally:
        if path and os.path.exists(path):
            os.remove(path)
