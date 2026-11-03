# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


# from config import *

from pyrogram import filters

from MeowMusic import app


@app.on_message(filters.command("dice"))
async def dice(bot, message):
    x = await bot.send_dice(message.chat.id)
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x = await bot.send_dice(message.chat.id, "🎯")
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🏀")
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


@app.on_message(filters.command("jackpots"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🎰")
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


@app.on_message(filters.command("ball"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🎳")
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


@app.on_message(filters.command("football"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "⚽")
    m = x.dice.value
    await message.reply_text(
        f"Hey {message.from_user.mention} your Score is : {m}", quote=True
    )


__help__ = """
 Play Game With Emojis:
/dice - Dice 🎲
/dart - Dart 🎯
/basket - Basket Ball 🏀
/ball - Bowling Ball 🎳
/football - Football ⚽
/jackpot - Spin slot machine 🎰
 """

__mod_name__ = "Dɪᴄᴇ"
