# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio

from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardButton, InlineKeyboardMarkup

from config import OWNER_ID
from MeowMusic import app
from MeowMusic.utils.database import is_command_locked

# --------------------------------------------------------------------------------- #

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = lambda text_size, text: (
    (text[:text_size] + "...").upper() if len(text) > text_size else text.upper()
)

# --------------------------------------------------------------------------------- #


async def get_userinfo_img(
    bg_path: str,
    font_path: str,
    user_id: int | str,
    profile_path: str | None = None,
):
    bg = Image.open(bg_path)

    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)

        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)

    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )

    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path


# --------------------------------------------------------------------------------- #

bg_path = "MeowMusic/assets/userinfo.jpg"
font_path = "MeowMusic/assets/hiroko.ttf"

# --------------------------------------------------------------------------------- #

# -------------


@app.on_chat_member_updated(filters.group, group=20)
async def member_has_left(client: app, member: ChatMemberUpdated):

    if await is_command_locked(member.chat.id, "left"):
        return

    if (
        not member.new_chat_member
        and member.old_chat_member.status not in {"banned", "left", "restricted"}
        and member.old_chat_member
    ):
        pass
    else:
        return

    user = member.old_chat_member.user if member.old_chat_member else member.from_user

    # Special Message For Bot Owner
    if user.id == OWNER_ID:
        await app.send_message(
            member.chat.id,
            f"Oʜ ɴᴏ! {user.mention} ʜᴀs ʟᴇғᴛ!\n**ᴄᴏɴᴛʀᴏʟ ɪs ɴᴏᴡ ɪɴ ᴀᴅᴍɪɴ's ʜᴀɴᴅs, ᴇɴᴊᴏʏ!**",
        )
        return

    # Check if the user has a profile photo
    if user.photo and user.photo.big_file_id:
        try:
            # Add the photo path, caption, and button details
            photo = await app.download_media(user.photo.big_file_id)

            welcome_photo = await get_userinfo_img(
                bg_path=bg_path,
                font_path=font_path,
                user_id=user.id,
                profile_path=photo,
            )

            caption = f"**#New_Member_Left**\n\n**๏** {user.mention} **ʜᴀs ʟᴇғᴛ ᴛʜɪs ɢʀᴏᴜᴘ**\n**๏ sᴇᴇ ʏᴏᴜ sᴏᴏɴ ᴀɢᴀɪɴ..!**"
            button_text = "๏ ᴠɪᴇᴡ ᴜsᴇʀ ๏"

            # Generate a deep link to open the user's profile
            deep_link = f"tg://openmessage?user_id={user.id}"

            # Send the message with the photo, caption, and button
            message = await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(button_text, url=deep_link)]]
                ),
            )

            # Schedule a task to delete the message after 30 seconds
            async def delete_message():
                await asyncio.sleep(20)
                await message.delete()

            # Run the task
            asyncio.create_task(delete_message())

        except RPCError as e:
            print(e)
            return
    else:
        # Handle the case where the user has no profile photo
        print(f"User {user.id} has no profile photo.")
