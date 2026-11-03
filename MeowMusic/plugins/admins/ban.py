# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import datetime

from pyrogram import enums, filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserAdminInvalid,
)
from pyrogram.types import ChatPermissions

from MeowMusic import app


def mention(user, name, mention=True):
    if mention == True:
        link = f"[{name}](tg://openmessage?user_id={user})"
    else:
        link = f"[{name}](https://t.me/{user})"
    return link


async def get_userid_from_username(username):
    try:
        user = await app.get_users(username)
    except:
        return None

    user_obj = [user.id, user.first_name]
    return user_obj


async def ban_user(
    user_id, first_name, admin_id, admin_name, chat_id, reason, time=None
):
    msg_text = ""
    try:
        await app.ban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        msg_text = "Bᴀɴ ʀɪɢʜᴛs? Nᴀʜ, I'ᴍ Jᴜsᴛ ʜᴇʀᴇ ғᴏʀ ᴛʜᴇ ᴅɪɢɪᴛᴀʟ ʜɪɢʜ-ғɪᴠᴇs 🙌\nGɪᴠᴇ ᴍᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs! 😡🥺"
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "I ᴡᴏɴᴛ ʙᴀɴ ᴀɴ ᴀᴅᴍɪɴ ʙʀᴜʜ!!"
        return msg_text, False
    except Exception as e:
        if user_id == 7355202884:
            msg_text = "Wʜʏ sʜᴏᴜʟᴅ I ʙᴀɴ ᴍʏ ᴏᴡɴᴇʀ? Sᴏʀʀʏ, ʙᴜᴛ I'ᴍ ɴᴏᴛ ᴀs sᴛᴜᴘɪᴅ ᴀs ʏᴏᴜ."
            return msg_text, False

        msg_text = f"opps!!\n{e}"
        return msg_text, False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text += ""
    msg_text += f"{user_mention} ɪs ʙᴀɴɴᴇᴅ ʙʏ {admin_mention}\n"

    if reason:
        msg_text += f"**Reason:** `{reason}`\n"
    if time:
        msg_text += f"**Time:** `{time}`\n"

    return msg_text, True


async def unban_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.unban_chat_member(chat_id, user_id)
    except ChatAdminRequired:
        msg_text = "Bᴀɴ ʀɪɢʜᴛs? Nᴀʜ, I'ᴍ Jᴜsᴛ ʜᴇʀᴇ ғᴏʀ ᴛʜᴇ ᴅɪɢɪᴛᴀʟ ʜɪɢʜ-ғɪᴠᴇs 🙌\nGɪᴠᴇ ᴍᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs! 😡🥺"
        return msg_text
    except Exception as e:
        msg_text = f"opps!!\n{e}"
        return msg_text

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text = f"{user_mention} ᴡᴀs ᴜɴʙᴀɴɴᴇᴅ ʙʏ {admin_mention}"
    return msg_text


async def mute_user(
    user_id, first_name, admin_id, admin_name, chat_id, reason, time=None
):
    msg_text = ""
    try:
        if time:
            mute_end_time = datetime.datetime.now() + time
            await app.restrict_chat_member(
                chat_id, user_id, ChatPermissions(), mute_end_time
            )
        else:
            await app.restrict_chat_member(chat_id, user_id, ChatPermissions())
    except ChatAdminRequired:
        msg_text = "Mᴜᴛᴇ ʀɪɢʜᴛs? Nᴀʜ, I'ᴍ Jᴜsᴛ ʜᴇʀᴇ ғᴏʀ ᴛʜᴇ ᴅɪɢɪᴛᴀʟ ʜɪɢʜ-ғɪᴠᴇs 🙌\nGɪᴠᴇ ᴍᴇ ᴍᴜᴛᴇ ʀɪɢʜᴛs! 😡🥺"
        return msg_text, False
    except UserAdminInvalid:
        msg_text = "I ᴡᴏɴᴛ ᴍᴜᴛᴇ ᴀɴ ᴀᴅᴍɪɴ ʙʀᴜʜ!!"
        return msg_text, False
    except Exception as e:
        if user_id == 7355202884:
            msg_text = (
                "Wʜʏ sʜᴏᴜʟᴅ I ᴍᴜᴛᴇ ᴍʏ ᴏᴡɴᴇʀ? Sᴏʀʀʏ, ʙᴜᴛ I'ᴍ ɴᴏᴛ ᴀs sᴛᴜᴘɪᴅ ᴀs ʏᴏᴜ."
            )
            return msg_text, False

        msg_text = f"opps!!\n{e}"
        return msg_text, False

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text += f"{user_mention} ɪs ᴍᴜᴛᴇᴅ ʙʏ {admin_mention}\n"

    if reason:
        msg_text += f"**Reason:** `{reason}`\n"
    if time:
        msg_text += f"**Time:** `{time}`\n"

    return msg_text, True


async def unmute_user(user_id, first_name, admin_id, admin_name, chat_id):
    try:
        await app.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(
                can_send_media_messages=True,
                can_send_messages=True,
                can_send_other_messages=True,
                can_send_polls=True,
                can_add_web_page_previews=True,
                can_invite_users=True,
            ),
        )
    except ChatAdminRequired:
        msg_text = "Mᴜᴛᴇ ʀɪɢʜᴛs? Nᴀʜ, I'ᴍ Jᴜsᴛ ʜᴇʀᴇ ғᴏʀ ᴛʜᴇ ᴅɪɢɪᴛᴀʟ ʜɪɢʜ-ғɪᴠᴇs 🙌\nGɪᴠᴇ ᴍᴇ ᴜɴᴍᴜᴛᴇ ʀɪɢʜᴛs! 😡🥺"
        return msg_text
    except Exception as e:
        msg_text = f"opps!!\n{e}"
        return msg_text

    user_mention = mention(user_id, first_name)
    admin_mention = mention(admin_id, admin_name)

    msg_text = f"{user_mention} ᴡᴀs ᴜɴᴍᴜᴛᴇᴅ ʙʏ {admin_mention}"
    return msg_text


@app.on_message(filters.command(["ban"]))
async def ban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ sᴏᴍᴇᴏɴᴇ"
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ sᴏᴍᴇᴏɴᴇ"
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            reason = message.text.split(None, 1)[1]
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                reason = message.text.partition(message.command[1])[2]
            except:
                reason = None

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ"
        )
        return

    msg_text, result = await ban_user(
        user_id, first_name, admin_id, admin_name, chat_id, reason
    )
    if result == True:
        await message.reply_text(msg_text)
    if result == False:
        await message.reply_text(msg_text)


@app.on_message(filters.command(["unban"]))
async def unban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴʙᴀɴ sᴏᴍᴇᴏɴᴇ."
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴʙᴀɴ sᴏᴍᴇᴏɴᴇ."
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj == None:
                return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
            user_id = user_obj[0]
            first_name = user_obj[1]

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ."
        )
        return

    msg_text = await unban_user(user_id, first_name, admin_id, admin_name, chat_id)
    await message.reply_text(msg_text)


@app.on_message(filters.command(["mute"]))
async def mute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            reason = message.text.split(None, 1)[1]
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                reason = message.text.partition(message.command[1])[2]
            except:
                reason = None

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
        reason = None
    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ"
        )
        return

    msg_text, result = await mute_user(
        user_id, first_name, admin_id, admin_name, chat_id, reason
    )
    if result == True:
        await message.reply_text(msg_text)

    if result == False:
        await message.reply_text(msg_text)


@app.on_message(filters.command(["unmute"]))
async def unmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        try:
            user_id = int(message.command[1])
            first_name = "User"
        except:
            user_obj = await get_userid_from_username(message.command[1])
            if user_obj == None:
                return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
            user_id = user_obj[0]
            first_name = user_obj[1]

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ."
        )
        return

    msg_text = await unmute_user(user_id, first_name, admin_id, admin_name, chat_id)
    await message.reply_text(msg_text)


@app.on_message(filters.command(["tmute"]))
async def tmute_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ sᴏᴍᴇᴏɴᴇ."
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            time = message.text.split(None, 1)[1]

            try:
                time_amount = time.split(time[-1])[0]
                time_amount = int(time_amount)
            except:
                return await message.reply_text(
                    "__wrong format!!__\n**Format:** `/tmute 2m`"
                )

            if time[-1] == "m":
                mute_duration = datetime.timedelta(minutes=time_amount)
            elif time[-1] == "h":
                mute_duration = datetime.timedelta(hours=time_amount)
            elif time[-1] == "d":
                mute_duration = datetime.timedelta(days=time_amount)
            else:
                return await message.reply_text(
                    "__wrong format!!__\n**Format:**\nm: Minutes\nh: Hours\nd: Days"
                )
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                time = message.text.partition(message.command[1])[2]
                try:
                    time_amount = time.split(time[-1])[0]
                    time_amount = int(time_amount)
                except:
                    return await message.reply_text(
                        "__wrong format!!__\n**Format:** `/tmute 2m`"
                    )

                if time[-1] == "m":
                    mute_duration = datetime.timedelta(minutes=time_amount)
                elif time[-1] == "h":
                    mute_duration = datetime.timedelta(hours=time_amount)
                elif time[-1] == "d":
                    mute_duration = datetime.timedelta(days=time_amount)
                else:
                    return await message.reply_text(
                        "__wrong format!!__\n**Format:**\nm: Minutes\nh: Hours\nd: Days"
                    )
            except:
                return await message.reply_text(
                    "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.\n**Format:** `/tmute @user 2m`"
                )

    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.\n**Format:** `/tmute [username] [time]`"
        )
        return

    msg_text, result = await mute_user(
        user_id,
        first_name,
        admin_id,
        admin_name,
        chat_id,
        reason=None,
        time=mute_duration,
    )
    if result == True:
        await message.reply_text(msg_text)
    if result == False:
        await message.reply_text(msg_text)


@app.on_message(filters.command(["tban"]))
async def tban_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name
    member = await chat.get_member(admin_id)
    if (
        member.status == enums.ChatMemberStatus.ADMINISTRATOR
        or member.status == enums.ChatMemberStatus.OWNER
    ):
        if member.privileges.can_restrict_members:
            pass
        else:
            msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ sᴏᴍᴇᴏɴᴇ."
            return await message.reply_text(msg_text)
    else:
        msg_text = "Yᴏᴜ ᴅᴏɴᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʙᴀɴ sᴏᴍᴇᴏɴᴇ."
        return await message.reply_text(msg_text)

    # Extract the user ID from the command or reply
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
            time = message.text.split(None, 1)[1]

            try:
                time_amount = time.split(time[-1])[0]
                time_amount = int(time_amount)
            except:
                return await message.reply_text(
                    "__wrong format!!__\n**Format:** `/tban 2m`"
                )

            if time[-1] == "m":
                ban_duration = datetime.timedelta(minutes=time_amount)
            elif time[-1] == "h":
                ban_duration = datetime.timedelta(hours=time_amount)
            elif time[-1] == "d":
                ban_duration = datetime.timedelta(days=time_amount)
            else:
                return await message.reply_text(
                    "__wrong format!!__\n**Format:**\nm: Minutes\nh: Hours\nd: Days"
                )
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj == None:
                    return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
                user_id = user_obj[0]
                first_name = user_obj[1]

            try:
                time = message.text.partition(message.command[1])[2]
                try:
                    time_amount = time.split(time[-1])[0]
                    time_amount = int(time_amount)
                except:
                    return await message.reply_text(
                        "__wrong format!!__\n**Format:** `/tban 2m`"
                    )

                if time[-1] == "m":
                    ban_duration = datetime.timedelta(minutes=time_amount)
                elif time[-1] == "h":
                    ban_duration = datetime.timedelta(hours=time_amount)
                elif time[-1] == "d":
                    ban_duration = datetime.timedelta(days=time_amount)
                else:
                    return await message.reply_text(
                        "__wrong format!!__\n**Format:**\nm: Minutes\nh: Hours\nd: Days"
                    )
            except:
                return await message.reply_text(
                    "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.\n**Format:** `/tban @user 2m`"
                )

    else:
        await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴀᴛ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ.\n**Format:** `/tban [username] [time]`"
        )
        return

    msg_text, result = await ban_user(
        user_id,
        first_name,
        admin_id,
        admin_name,
        chat_id,
        reason=None,
        time=ban_duration,
    )
    if result == True:
        await message.reply_text(msg_text)
    if result == False:
        await message.reply_text(msg_text)


@app.on_message(filters.command("sban") & filters.group)
async def silent_ban(client, message):
    await message.delete()
    chat_id = message.chat.id
    from_user = message.from_user

    try:
        member = await app.get_chat_member(chat_id, from_user.id)
        if not (
            member.status in ("administrator", "creator")
            and member.can_restrict_members
        ):
            return
    except Exception:
        return

    user_id = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        try:
            await message.reply_to_message.delete()
        except Exception:
            pass
    elif len(message.command) >= 2:
        user_handle = message.text.split(None, 1)[1].strip()
        try:
            user = await app.get_users(user_handle)
            user_id = user.id
        except Exception:
            return
    else:
        return

    if not user_id:
        return

    # Final ban
    try:
        await app.ban_chat_member(chat_id, user_id)
    except Exception:
        pass
