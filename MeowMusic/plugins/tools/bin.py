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


@app.on_message(filters.command(["bin", "ccbin", "bininfo"], [".", "!", "/"]))
async def check_ccbin(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Please Give Me a Bin To\nGet Bin Details !</b>"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("<b>Checking ...</b>")
    bin = message.text.split(None, 1)[1]
    if len(bin) < 6:
        return await aux.edit("<b>❌ Wrong Bin❗...</b>")
    try:
        resp = await api.bininfo(bin)
        await aux.edit(f"""
<b> 𝗩𝗔𝗟𝗜𝗗 𝗕𝗜𝗡 ✅</b>

<b>🏦 𝗕𝗔𝗡𝗞➪</b> <tt>{resp.bank}</tt>
<b>💳 𝗕𝗜𝗡➪</b> <tt>{resp.bin}</tt>
<b>🏡 𝗖𝗢𝗨𝗡𝗧𝗥𝗬➪</b> <tt>{resp.country}</tt>
<b>🇮🇳 𝗙𝗟𝗔𝗚➪</b> <tt>{resp.flag}</tt>
<b>🧿 𝗜𝗦𝗢➪</b> <tt>{resp.iso}</tt>
<b>⏳ 𝗟𝗘𝗩𝗘𝗟➪</b> <tt>{resp.level}</tt>
<b>🔴 𝗣𝗥𝗘𝗣𝗔𝗜𝗗➪</b> <tt>{resp.prepaid}</tt>
<b>🆔 𝗧𝗬𝗣𝗘➪</b> <tt>{resp.type}</tt>
<b>ℹ️ 𝗩𝗘𝗡𝗗𝗢𝗥➪</b> <tt>{resp.vendor}</tt>""")
    except:
        return await aux.edit("""
🚫 BIN not recognized. Please enter a valid BIN.""")
