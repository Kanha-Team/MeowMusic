# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import os
import re
import tempfile
from uuid import uuid4

import pyrogram
from PIL import Image
from pyrogram import filters
from pyrogram.raw import functions, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID
from MeowMusic import app
from MeowMusic.utils.database import is_command_locked

######### sticker id


@app.on_message(filters.command("st"))
def generate_sticker(client, message):
    if len(message.command) == 2:
        sticker_id = message.command[1]
        try:
            client.send_sticker(message.chat.id, sticker=sticker_id)
        except Exception as e:
            message.reply_text(f"Error: {e}")
    else:
        message.reply_text("Please provide a sticker ID after /st command.")


# ---------


@app.on_message(filters.command("packkang"))
async def _packkang(app: app, message):

    if await is_command_locked(message.chat.id, "packkang"):
        return

    txt = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ....**")
    if not message.reply_to_message:
        await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ")
        return
    if not message.reply_to_message.sticker:
        await txt.edit("ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ")
        return
    if (
        message.reply_to_message.sticker.is_animated
        or message.reply_to_message.sticker.is_video
    ):
        return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɴᴏɴ-ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ")
    if len(message.command) < 2:
        pack_name = "SticksPro - @LordKanha"
    else:
        pack_name = message.text.split(maxsplit=1)[1]
    short_name = message.reply_to_message.sticker.set_name
    stickers = await app.invoke(
        pyrogram.raw.functions.messages.GetStickerSet(
            stickerset=pyrogram.raw.types.InputStickerSetShortName(
                short_name=short_name
            ),
            hash=0,
        )
    )
    shits = stickers.documents
    sticks = []

    for i in shits:
        sex = pyrogram.raw.types.InputDocument(
            id=i.id, access_hash=i.access_hash, file_reference=i.thumbs[0].bytes
        )

        sticks.append(
            pyrogram.raw.types.InputStickerSetItem(
                document=sex, emoji=i.attributes[1].alt
            )
        )

    try:
        if pack_name != "SticksPro - @SticksPro":
            sanitized_name = re.sub(r"[^a-zA-Z0-9_]", "", pack_name)
            short_name = f"SticksPro_{sanitized_name}_by_{app.me.username}"
            # short_name = f'SticksPro_{pack_name}_by_{app.me.username}'
        else:
            short_name = (
                f'SticksPro_{str(uuid4()).replace("-","")}_by_{app.me.username}'
            )
        user_id = await app.resolve_peer(message.from_user.id)
        await app.invoke(
            pyrogram.raw.functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=short_name,
                stickers=sticks,
            )
        )
        await txt.edit(
            f"**ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴋᴀɴɢᴇᴅ ʟɪɴᴋ**!\n**ᴛᴏᴛᴀʟ sᴛɪᴄᴋᴇʀ **: {len(sticks)}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ᴘᴀᴄᴋ ʟɪɴᴋ", url=f"http://t.me/addstickers/{short_name}"
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        await message.reply(str(e))


###### sticker id =
@app.on_message(filters.command(["stickerid", "stid"]))
async def sticker_id(app: app, msg):
    if not msg.reply_to_message or not msg.reply_to_message.sticker:
        await msg.reply_text("Reply to a sticker")
    st_in = msg.reply_to_message.sticker
    await msg.reply_text(f"""
⊹ <u>**sᴛɪᴄᴋᴇʀ ɪɴғᴏ**</u> ⊹
**⊚ sᴛɪᴄᴋᴇʀ ɪᴅ **: `{st_in.file_id}`\n
**⊚ sᴛɪᴄᴋᴇʀ ᴜɴɪǫᴜᴇ ɪᴅ **: `{st_in.file_unique_id}`
""")


#####


@app.on_message(filters.command("stdl") & filters.reply)
async def download_sticker(client, message):
    proc = await message.reply_text("downloading…")
    st = message.reply_to_message.sticker
    with tempfile.TemporaryDirectory() as td:
        path = await message.reply_to_message.download(os.path.join(td, "st"))
        if st.is_animated:
            await proc.edit("➣ sending .tgs…")
            await client.send_document(
                message.chat.id, path, caption="here's your animated sticker!"
            )
        elif st.is_video:
            await proc.edit("➣ sending video…")
            await client.send_video(
                message.chat.id,
                path,
                supports_streaming=True,
                caption="here's your video sticker!",
            )
        else:
            await proc.edit("➣ converting to png…")
            img = Image.open(path)
            out = f"{path}.png"
            img.save(out, "PNG")
            await client.send_photo(
                message.chat.id, out, caption="here's your static image!"
            )
    await proc.delete()


######


# ======================================================================


import asyncio

from pyrogram import filters

from MeowMusic import app

CHANNEL_ID = -1004449204699


@app.on_message(filters.command("packsticker") & filters.user(OWNER_ID))
async def _packkang(client, message):
    txt = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ....**")
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ")

    sticker = message.reply_to_message.sticker

    if len(message.command) < 2:
        pack_name = "SticksPro - @LordKanha"
        old_pack_name = "SticksPro"
    else:
        old_pack_name = message.text.split(maxsplit=1)[1]
        pack_name = old_pack_name + " :: @LordKanha"

    # fetch full set
    short_name = sticker.set_name
    stickerset = await client.invoke(
        functions.messages.GetStickerSet(
            stickerset=types.InputStickerSetShortName(short_name=short_name),
            hash=0,
        )
    )
    docs = stickerset.documents

    if not docs:
        return await txt.edit("No stickers found in this pack.")

    # generate unique short_name
    if pack_name != "SticksPro - @LordKanha":
        sanitized_name = re.sub(r"[^a-zA-Z0-9_]", "", old_pack_name)
        new_short = f"{sanitized_name}_by_{client.me.username}"
    else:
        new_short = f"{uuid4().hex}_by_{client.me.username}"

    user_id = await client.resolve_peer(message.from_user.id)

    first_doc = docs[0]
    sex = types.InputDocument(
        id=first_doc.id,
        access_hash=first_doc.access_hash,
        file_reference=first_doc.file_reference,
    )
    emoji = "🌸"
    for attr in first_doc.attributes:
        if isinstance(attr, types.DocumentAttributeSticker):
            emoji = attr.alt or "🌸"
            break

    try:
        await client.invoke(
            functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=new_short,
                stickers=[types.InputStickerSetItem(document=sex, emoji=emoji)],
            )
        )
    except Exception as e:
        return await txt.edit(f"Failed to create set:\n\n{e}")

    added = 1
    failed = 0

    for i in docs[1:]:
        sex = types.InputDocument(
            id=i.id,
            access_hash=i.access_hash,
            file_reference=i.file_reference,
        )
        emoji = "🌸"
        for attr in i.attributes:
            if isinstance(attr, types.DocumentAttributeSticker):
                emoji = attr.alt or "🌸"
                break

        try:
            await client.invoke(
                functions.stickers.AddStickerToSet(
                    stickerset=types.InputStickerSetShortName(short_name=new_short),
                    sticker=types.InputStickerSetItem(document=sex, emoji=emoji),
                )
            )
            added += 1
            await asyncio.sleep(0.3)
        except Exception:
            failed += 1
            continue

    pack_link = f"http://t.me/addstickers/{new_short}"

    await client.send_message(
        CHANNEL_ID,
        f"**✨ ɴᴇᴡ ᴘᴀᴄᴋ**\n\n - **ɴᴀᴍᴇ **: [{old_pack_name}]({pack_link})\n - **ᴛᴏᴛᴀʟ sᴛɪᴄᴋᴇʀ **: {added}\n\n - @LordKanha",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"{old_pack_name}", url=pack_link)]]
        ),
    )

    await txt.edit(
        f"**ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴘᴀᴄᴋ!**\n\n✅ Added: {added}\n❌ Failed: {failed}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴘᴀᴄᴋ ʟɪɴᴋ", url=pack_link)]]
        ),
    )


# ================================================================


@app.on_message(filters.command("sendsticker") & filters.user(OWNER_ID))
async def send_sticker_to_channel(client, message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ sᴇɴᴅ ɪᴛ ᴛᴏ ᴄʜᴀɴɴᴇʟ")

    sticker = message.reply_to_message.sticker

    # get optional command text
    cmd_text = " ".join(message.command[1:]) if len(message.command) > 1 else None

    pack_link = None

    # fetch full set info
    if sticker.set_name:
        try:
            await client.invoke(
                functions.messages.GetStickerSet(
                    stickerset=types.InputStickerSetShortName(
                        short_name=sticker.set_name
                    ),
                    hash=0,
                )
            )
            pack_link = f"http://t.me/addstickers/{sticker.set_name}"
        except Exception:
            pack_link = None

    # inline button
    buttons = []
    if pack_link:
        button_text = cmd_text if cmd_text else "ᴀᴅᴅ ᴘᴀᴄᴋ"
        buttons.append([InlineKeyboardButton(button_text, url=pack_link)])

    await client.send_sticker(
        chat_id=CHANNEL_ID,
        sticker=sticker.file_id,
        reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
    )

    await message.reply_text("✅ Sticker sent to channel with pack link!")
