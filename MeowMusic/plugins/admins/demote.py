# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters
from pyrogram.types import ChatPrivileges, Message

from MeowMusic import app


@app.on_message(filters.command("demote") & filters.group)
async def demote_user(client, message: Message):
    chat = message.chat
    replied = message.reply_to_message
    args = message.text.split()

    bot_member = await client.get_chat_member(chat.id, app.me.id)
    if not bot_member.privileges or not bot_member.privileges.can_promote_members:
        return await message.reply(
            "__I don't have permission to manage admin rights!__"
        )

    sender = await client.get_chat_member(chat.id, message.from_user.id)
    if not sender.privileges or not sender.privileges.can_promote_members:
        return await message.reply("__You don't have permission to demote others!__")

    # Get target user
    if replied:
        user = replied.from_user
    elif len(args) >= 2:
        try:
            user = await client.get_users(args[1])
        except Exception:
            return await message.reply("__Couldn't find that user.__")
    else:
        return await message.reply("__Reply to a user or provide user ID/username.__")

    if user.id == message.from_user.id:
        return await message.reply("__You can't demote yourself!__")

    try:
        target = await client.get_chat_member(chat.id, user.id)
    except:
        return await message.reply("__This user is not in the group.__")

    if not target.privileges:
        return await message.reply("__This user is not an admin.__")

    if not target.can_be_edited:
        return await message.reply(
            "__I can't change this user's rights... and I'm not allowed to touch them.__"
        )

    try:
        await client.promote_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ),
        )
        await message.reply("Demoted !")
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            return await message.reply(
                "__I don't have enough rights to demote this admin.__"
            )
        return await message.reply("__Failed to demote that user:__")
