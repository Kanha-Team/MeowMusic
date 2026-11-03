# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio
import random

import aiohttp
from pyrogram import filters
from pyrogram.enums import ChatAction, PollType

from MeowMusic import app
from MeowMusic.misc import SUDOERS

last_command_time = {}
active_quizzes = {}


@app.on_message(filters.command(["quiz"]))
async def quiz(client, message):
    user_id = message.from_user.id

    if user_id not in SUDOERS:
        return await message.reply("Tᴀᴋɪɴɢ ᴀ ǫᴜɪᴄᴋ ʙʀᴇᴀᴋ! Qᴜɪᴢ ᴡɪʟʟ ʙᴇ ʙᴀᴄᴋ sᴏᴏɴ..")

    current_time = asyncio.get_event_loop().time()
    args = message.text.split()

    # --- Stop Command ---
    if len(args) > 1 and args[1].lower() == "stop":
        if active_quizzes.get(user_id):
            active_quizzes[user_id] = False
            await message.reply_text("__Quiz stopped successfully.__")
        else:
            await message.reply_text("__No active quiz session to stop.__")
        return

    # --- Rate Limit ---
    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text("__Please wait 5 seconds before using this again.__")
        return

    last_command_time[user_id] = current_time
    num_quizzes = 1

    if len(args) > 1 and args[1].isdigit():
        if int(args[1]) > 30:
            await message.reply_text(
                "__You can't request more than 30 quizzes at once!__"
            )
            return
        num_quizzes = int(args[1])

    # categories = [9, 20, 21]  # GK, Mythology, Sports
    categories = [9, 20, 21]

    active_quizzes[user_id] = True

    async with aiohttp.ClientSession() as session:
        for i in range(num_quizzes):
            if not active_quizzes.get(user_id):
                break

            await app.send_chat_action(message.chat.id, ChatAction.TYPING)

            url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
            async with session.get(url) as resp:
                response = await resp.json()

            if response.get("response_code") != 0 or "results" not in response:
                await message.reply_text("⚠️ Couldn't fetch quiz. Try again later!")
                continue

            data = response["results"][0]
            question = data["question"]
            correct_answer = data["correct_answer"]
            incorrect_answers = data["incorrect_answers"]

            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)
            cid = all_answers.index(correct_answer)

            await app.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=all_answers,
                is_anonymous=False,
                type=PollType.QUIZ,
                correct_option_id=cid,
                open_period=12,
                explanation="JOIN - @ProBotsHQ",
            )

            if i < num_quizzes - 1:
                await asyncio.sleep(14)

    active_quizzes[user_id] = False
