# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import enums, filters

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


# ✅ Kick Command
@app.on_message(filters.command(["kick"]))
async def kick_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    admin_id = message.from_user.id
    admin_name = message.from_user.first_name

    # Check if the user is an admin
    member = await chat.get_member(admin_id)
    if member.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴋɪᴄᴋ ᴜsᴇʀs.")

    if not member.privileges.can_restrict_members:
        return await message.reply_text("Yᴏᴜ ʟᴀᴄᴋ ᴛʜᴇ ᴘʀɪᴠɪʟᴇɢᴇ ᴛᴏ ᴋɪᴄᴋ ᴜsᴇʀs.")

    # Extract the target user
    if len(message.command) > 1:
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
            first_name = message.reply_to_message.from_user.first_name
        else:
            try:
                user_id = int(message.command[1])
                first_name = "User"
            except:
                user_obj = await get_userid_from_username(message.command[1])
                if user_obj is None:
                    return await message.reply_text("I ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
                user_id = user_obj[0]
                first_name = user_obj[1]
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        first_name = message.reply_to_message.from_user.first_name
    else:
        return await message.reply_text(
            "Pʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ."
        )

    # Check if the bot is an admin
    bot_member = await chat.get_member(client.me.id)
    if bot_member.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text(
            "I ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs ᴛᴏ ᴋɪᴄᴋ ᴜsᴇʀs. Gʀᴀɴᴛ ᴍᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ!"
        )

    # Admin protection check
    target_member = await chat.get_member(user_id)
    if target_member.status in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("__I ᴡᴏɴ'ᴛ ᴋɪᴄᴋ ᴀɴ ᴀᴅᴍɪɴ !__")

    if not bot_member.privileges.can_restrict_members:
        return await message.reply_text(
            "ɪ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ... ʙᴜᴛ I’ᴍ ᴍɪssɪɴɢ ᴍʏ sᴜᴘᴇʀᴘᴏᴡᴇʀs."
        )

    # Kick the user
    try:
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)
        user_mention = mention(user_id, first_name)
        admin_mention = mention(admin_id, admin_name)
        await message.reply_text(f"{user_mention} ɪs ᴋɪᴄᴋᴇᴅ ʙʏ {admin_mention}. 🚀")
    except Exception as e:
        await message.reply_text(f"__Oops! Something went wrong:__\n`{e}`")


# ✅ KickMe Command
@app.on_message(filters.command(["kickme"]))
async def kickme_command_handler(client, message):
    chat = message.chat
    chat_id = chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Check if the bot is an admin
    bot_member = await chat.get_member(client.me.id)
    if bot_member.status not in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text(
            "I ɴᴇᴇᴅ ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs ᴛᴏ ᴋɪᴄᴋ ᴜsᴇʀs. Gʀᴀɴᴛ ᴍᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ!"
        )

    # Check if the user is an admin
    member = await chat.get_member(user_id)
    if member.status in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ]:
        return await message.reply_text("ɪ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ... ʙᴜᴛ ʏᴏᴜ'ʀᴇ ᴀɴ ᴀᴅᴍɪɴ.")

    if not bot_member.privileges.can_restrict_members:
        return await message.reply_text(
            "ɪ ᴡɪsʜ ɪ ᴄᴏᴜʟᴅ... ʙᴜᴛ I’ᴍ ᴍɪssɪɴɢ ᴍʏ sᴜᴘᴇʀᴘᴏᴡᴇʀs."
        )

    # Kick the user
    try:
        await app.ban_chat_member(chat_id, user_id)
        await app.unban_chat_member(chat_id, user_id)
        user_mention = mention(user_id, first_name)
        await message.reply_text(f"{user_mention}, ʏᴏᴜ Jᴜsᴛ ᴋɪᴄᴋᴇᴅ ʏᴏᴜʀsᴇʟғ. !")
    except Exception as e:
        await message.reply_text(f"__Oops! Something went wrong:__\n`{e}`")
