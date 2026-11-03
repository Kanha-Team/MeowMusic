# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait

from config import MAIN_OWNER, OWNER_ID, adminlist
from MeowMusic import app
from MeowMusic.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_served_chats,
    get_served_users,
)
from MeowMusic.utils.decorators.language import language
from MeowMusic.utils.formatters import alpha_to_int

IS_BROADCASTING = False


def owner_or_special_user(_, __, message):
    return message.from_user.id in {OWNER_ID, 8617644501}


# @app.on_message(filters.command("broadcast") & SUDOERS)
@app.on_message(filters.command("broadcast") & filters.create(owner_or_special_user))
@language
async def braodcast_message(client, message, _):
    """
    if message.from_user.id != MAIN_OWNER:
        return await message.reply_text(
            f"» 🚀 Wᴀɴᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴏᴡɴ ᴍᴇssᴀɢᴇs?\n\nUɴʟᴏᴄᴋ ᴇxᴄʟᴜsɪᴠᴇ ᴀᴄᴄᴇss ᴡɪᴛʜ ᴏᴜʀ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ᴘʟᴀɴ!\n Jᴏɪɴ [PʀᴏBᴏᴛs]({SUPPORT_CHAT}) ᴏʀ DM @KanhaXD ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs ᴀɴᴅ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ !"
        )
    """

    # send log msg to owner about broadcast
    await app.send_message(
        chat_id=MAIN_OWNER,
        text=f"#owner \n\n{message.from_user.mention} Jᴜsᴛ Bʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
    )

    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_8"])

    IS_BROADCASTING = True
    await message.reply_text(_["broad_1"])

    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                sent += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text(_["broad_3"].format(sent, pin))
        except:
            pass

    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
                await asyncio.sleep(0.2)
            except FloodWait as fw:
                flood_time = int(fw.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(_["broad_4"].format(susr))
        except:
            pass

    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_5"])
        text = _["broad_6"]
        from MeowMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                try:
                    (
                        await client.forward_messages(dialog.chat.id, y, x)
                        if message.reply_to_message
                        else await client.send_message(dialog.chat.id, text=query)
                    )
                    sent += 1
                    await asyncio.sleep(3)
                except FloodWait as fw:
                    flood_time = int(fw.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except:
                    continue
            text += _["broad_7"].format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass
    IS_BROADCASTING = False

    # await app.send_message(
    #             chat_id=SUB_LOG,
    #             text=f"#owner \n\n{message.from_user.mention} Jᴜsᴛ Bʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
    #         )


async def auto_clean():
    while not await asyncio.sleep(10):
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    async for user in app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    ):
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())
