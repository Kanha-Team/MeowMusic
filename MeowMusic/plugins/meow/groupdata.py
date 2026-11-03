# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import time
from asyncio import sleep

from pyrogram import enums, filters

from MeowMusic import app


@app.on_message(~filters.private & filters.command(["groupdata"]), group=2)
async def instatus(app, message):
    start_time = time.perf_counter()
    user = await app.get_chat_member(message.chat.id, message.from_user.id)
    count = await app.get_chat_members_count(message.chat.id)
    if user.status in (
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER,
    ):
        sent_message = await message.reply_text("GETTING INFORMATION...")
        deleted_acc = 0
        premium_acc = 0
        banned = 0
        bot = 0
        uncached = 0
        async for ban in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.BANNED
        ):
            banned += 1
        async for member in app.get_chat_members(message.chat.id):
            user = member.user
            if user.is_deleted:
                deleted_acc += 1
            elif user.is_bot:
                bot += 1
            elif user.is_premium:
                premium_acc += 1
            else:
                uncached += 1
        end_time = time.perf_counter()
        timelog = f"{end_time - start_time:.2f}"
        await sent_message.edit(f"""
**➖➖➖➖➖➖➖
➲ NAME : {message.chat.title} ✅
➲ MEMBERS : [ {count} ]🫂
➖➖➖➖➖➖➖
➲ BOTS : {bot}💡
➲ ZOMBIES : {deleted_acc}🧟
➲ BANNED : {banned}🚫
➲ PREMIUM USERS : {premium_acc}🎁
➖➖➖➖➖➖➖
TIME TAKEN : {timelog} S**""")
    else:
        sent_message = await message.reply_text("ONLY ADMINS CAN USE THIS !")
        await sleep(5)
        await sent_message.delete()
