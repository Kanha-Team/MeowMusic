# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import enums, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MeowMusic import app


@app.on_callback_query(filters.regex(r"^unpin"))
async def unpin_callbacc(client, CallbackQuery):
    user_id = CallbackQuery.from_user.id
    chat_id = CallbackQuery.message.chat.id
    member = await app.get_chat_member(chat_id, user_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_pin_messages:
            pass
        else:
            await CallbackQuery.answer("You dont have rights, meow!", show_alert=True)
            return
    else:
        await CallbackQuery.answer("You dont have rights, meow!", show_alert=True)
        return

    msg_id = CallbackQuery.data.split("=")[1]
    try:
        msg_id = int(msg_id)
    except:
        if msg_id == "yes":
            await client.unpin_all_chat_messages(chat_id)
            textt = "I have unpinned all the pinned messages"
        else:
            textt = "Ok, i wont unpin all the messages"

        await CallbackQuery.message.edit_caption(
            textt,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Delete", callback_data="delete_btn=admin"
                        )
                    ]
                ]
            ),
        )
        return

    await client.unpin_chat_message(chat_id, msg_id)
    await CallbackQuery.message.edit_caption(
        "unpinned!!",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Delete", callback_data="delete_btn=admin")]]
        ),
    )


@app.on_message(filters.command(["unpinall"]))
async def unpin_command_handler(client, message):
    chat = message.chat
    admin_id = message.from_user.id
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_pin_messages:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴘɪɴ sᴏᴍᴇᴛʜɪɴɢ"
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴘɪɴ sᴏᴍᴇᴛʜɪɴɢ"
        return await message.reply_text(msg_text)

    await message.reply_text(
        "**Aʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴᴘɪɴ ᴀʟʟ ᴛʜᴇ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ᴄʜᴀᴛ??**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="𝐘‌єs", callback_data="unpinall=yes"),
                    InlineKeyboardButton(text="𝐍‌σ", callback_data="unpinall=no"),
                ]
            ]
        ),
    )
