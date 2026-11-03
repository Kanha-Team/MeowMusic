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


@app.on_message(filters.command("promote") & filters.group)
async def promote_user(client, message: Message):
    chat = message.chat
    replied = message.reply_to_message
    args = message.text.split(None, 2)

    bot_member = await client.get_chat_member(chat.id, app.me.id)
    if not bot_member.privileges or not bot_member.privileges.can_promote_members:
        return await message.reply("__I don't have permission to promote members!__")

    sender = await client.get_chat_member(chat.id, message.from_user.id)
    if not sender.privileges or not sender.privileges.can_promote_members:
        return await message.reply("__You aren't allowed to promote members.__")

    # Get target user
    if replied:
        user = replied.from_user
        title = " ".join(args[1:]) if len(args) > 1 else None
    elif len(args) >= 2:
        user_identifier = args[1]
        try:
            user = await client.get_users(user_identifier)
        except:
            return await message.reply("__Couldn't find that user.__")
        title = " ".join(args[2:]) if len(args) > 2 else None
    else:
        return await message.reply("__Reply to a user or give user ID/username.__")

    try:
        target = await client.get_chat_member(chat.id, user.id)
        if target.status in ["administrator", "creator"]:
            return await message.reply("__This user is already an admin.__")
    except:
        return await message.reply("__This user is not in the group.__")

    if title and len(title) > 16:
        return await message.reply("__Title too long! Keep it under 16 characters.__")

    # Promote
    try:
        bot_member = await client.get_chat_member(chat.id, app.me.id)
        bot_privs = bot_member.privileges

        sender = await client.get_chat_member(chat.id, message.from_user.id)
        if sender.status == "creator":
            sender_privs = None
        else:
            sender_privs = sender.privileges

        bool(bot_privs and bot_privs.can_change_info) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_change_info)
        )

        is_invite_users = bool(bot_privs and bot_privs.can_invite_users) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_invite_users)
        )

        is_delete_messages = bool(bot_privs and bot_privs.can_delete_messages) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_delete_messages)
        )

        bool(bot_privs and bot_privs.can_restrict_members) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_restrict_members)
        )

        is_pin_messages = bool(bot_privs and bot_privs.can_pin_messages) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_pin_messages)
        )

        is_manage_chat = bool(bot_privs and bot_privs.can_manage_chat) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_manage_chat)
        )

        is_manage_video_chats = bool(
            bot_privs and bot_privs.can_manage_video_chats
        ) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_manage_video_chats)
        )

        await client.promote_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=is_invite_users,
                can_delete_messages=is_delete_messages,
                can_restrict_members=False,
                can_pin_messages=is_pin_messages,
                can_promote_members=False,
                can_manage_chat=is_manage_chat,
                can_manage_video_chats=is_manage_video_chats,
            ),
        )

        # Set title
        if title:
            await client.set_administrator_title(
                chat_id=chat.id, user_id=user.id, title=title
            )
            await message.reply("Promoted!")
        else:
            await message.reply("Promoted!")
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.reply(
                "__I can't change this user's rights... they're already an admin, and I'm not allowed to touch them.__"
            )

        elif "ADMIN_RANK_INVALID" in str(e):
            await message.reply(
                "__The custom admin title is invalid or too long. Please keep it under 16 characters.__"
            )
        else:
            await message.reply("__Failed to promote:__")


@app.on_message(filters.command("fullpromote") & filters.group)
async def fullpromote_user(client, message: Message):
    chat = message.chat
    replied = message.reply_to_message
    args = message.text.split(None, 2)

    bot_member = await client.get_chat_member(chat.id, app.me.id)
    if not bot_member.privileges or not bot_member.privileges.can_promote_members:
        return await message.reply("__I don't have permission to promote members!__")

    sender = await client.get_chat_member(chat.id, message.from_user.id)
    if not sender.privileges or not sender.privileges.can_promote_members:
        return await message.reply("__You aren't allowed to promote members.__")

    # Get target user
    if replied:
        user = replied.from_user
        title = " ".join(args[1:]) if len(args) > 1 else None
    elif len(args) >= 2:
        user_identifier = args[1]
        try:
            user = await client.get_users(user_identifier)
        except:
            return await message.reply("__Couldn't find that user.__")
        title = " ".join(args[2:]) if len(args) > 2 else None
    else:
        return await message.reply("__Reply to a user or give user ID/username.__")

    try:
        target = await client.get_chat_member(chat.id, user.id)
        if target.status in ["administrator", "creator"]:
            return await message.reply("__This user is already an admin.__")
    except:
        return await message.reply("__This user is not in the group.__")

    if title and len(title) > 16:
        return await message.reply("__Title too long! Keep it under 16 characters.__")

    # Promote
    try:
        bot_member = await client.get_chat_member(chat.id, app.me.id)
        bot_privs = bot_member.privileges

        sender = await client.get_chat_member(chat.id, message.from_user.id)
        if sender.status == "creator":
            sender_privs = None
        else:
            sender_privs = sender.privileges

        is_change_info = bool(bot_privs and bot_privs.can_change_info) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_change_info)
        )

        is_invite_users = bool(bot_privs and bot_privs.can_invite_users) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_invite_users)
        )

        is_delete_messages = bool(bot_privs and bot_privs.can_delete_messages) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_delete_messages)
        )

        is_restrict_members = bool(bot_privs and bot_privs.can_restrict_members) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_restrict_members)
        )

        is_pin_messages = bool(bot_privs and bot_privs.can_pin_messages) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_pin_messages)
        )

        is_manage_chat = bool(bot_privs and bot_privs.can_manage_chat) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_manage_chat)
        )

        is_manage_video_chats = bool(
            bot_privs and bot_privs.can_manage_video_chats
        ) and (
            sender.status == "creator"
            or (sender_privs and sender_privs.can_manage_video_chats)
        )

        await client.promote_chat_member(
            chat_id=chat.id,
            user_id=user.id,
            privileges=ChatPrivileges(
                can_change_info=is_change_info,
                can_invite_users=is_invite_users,
                can_delete_messages=is_delete_messages,
                can_restrict_members=is_restrict_members,
                can_pin_messages=is_pin_messages,
                can_promote_members=True,
                can_manage_chat=is_manage_chat,
                can_manage_video_chats=is_manage_video_chats,
            ),
        )

        # Set title
        if title:
            await client.set_administrator_title(
                chat_id=chat.id, user_id=user.id, title=title
            )
            await message.reply("fullromoted!")
        else:
            await message.reply("fullpromoted!")
    except Exception as e:
        if "CHAT_ADMIN_REQUIRED" in str(e):
            await message.reply(
                "__I can't change this user's rights... they're already an admin, and I'm not allowed to touch them.__"
            )

        elif "ADMIN_RANK_INVALID" in str(e):
            await message.reply(
                "__The custom admin title is invalid or too long. Please keep it under 16 characters.__"
            )
        else:
            await message.reply("__Failed to promote:__")
