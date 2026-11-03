# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio

from pyrogram import filters

from config import OWNER_ID
from MeowMusic import app

spamming = {}


# Define the spam command handler
@app.on_message(filters.command("raid", prefixes="/") & filters.user(OWNER_ID))
async def send_spam_message(client, message):
    chat_id = message.chat.id
    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        return await message.reply("Usage: /raid <count> <message>")

    try:
        count = int(args[1])
        text = args[2]
    except ValueError:
        return await message.reply("Invalid count! Please enter a number.")

    spamming[chat_id] = True

    for _ in range(min(count, 100)):
        if not spamming.get(chat_id):
            return await message.reply("✅ Raid Stopped!")

        await client.send_message(chat_id, text)
        await asyncio.sleep(1)


@app.on_message(filters.command("stopraid", prefixes="/") & filters.user(OWNER_ID))
async def stop_spam(client, message):
    chat_id = message.chat.id

    if chat_id in spamming:
        spamming[chat_id] = False
    else:
        await message.reply("No active raid found!")


# Define the spam command handler
@app.on_message(
    filters.command(["uraid"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & filters.user(OWNER_ID)
)
async def mention_spam(client, message):
    if not message.reply_to_message:
        return await message.reply("Please reply to a user!")

    replied_user_id = message.reply_to_message.from_user.id

    if replied_user_id == OWNER_ID and message.from_user.id != OWNER_ID:
        return await message.reply("Ye Kya Bak Rhe Ho ....")

    args = message.text.split(maxsplit=2)

    if len(args) < 3:
        return await message.reply("Usage: /uraid <count> <message>")

    try:
        count = int(args[1])
        text = args[2]
    except ValueError:
        return await message.reply("Invalid count! Please enter a number.")

    target_user = message.reply_to_message.from_user
    mention = f"[{target_user.first_name}](tg://user?id={target_user.id})"

    for _ in range(count):
        await client.send_message(message.chat.id, f"{mention} {text}")
        await asyncio.sleep(1.5)
