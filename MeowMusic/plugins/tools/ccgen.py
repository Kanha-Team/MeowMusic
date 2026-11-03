# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import *
from pyrogram.types import *

from ... import *


@app.on_message(filters.command(["gen", "ccgen"], [".", "!", "/"]))
async def gen_cc(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please Give Me a Bin To\nGenerate Cc ...**")
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("**Generating ...**")
    bin = message.text.split(None, 1)[1]
    if len(bin) < 6:
        return await aux.edit("**❌ Wrong Bin❗...**")
    try:
        resp = await api.ccgen(bin, 10)
        cards = resp.liveCC
        await aux.edit(f"""
**💠 Some Live Generated CC:**
`{cards[0]}`\n`{cards[1]}`\n`{cards[2]}`
`{cards[3]}`\n`{cards[4]}`\n`{cards[5]}`
`{cards[6]}`\n`{cards[7]}`\n`{cards[8]}`
`{cards[9]}`
**💳 Bin:** `{resp.results[0].bin}`
**⏳ Time Took:** `{resp.took}`\n\n""")
    except Exception as e:
        return await aux.edit(f"**Error:** `{e}`")
