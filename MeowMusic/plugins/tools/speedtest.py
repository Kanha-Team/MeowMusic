# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import speedtest
from pyrogram import filters
from pyrogram.types import Message

from MeowMusic import app
from MeowMusic.misc import SUDOERS
from MeowMusic.utils.decorators.language import language


async def testspeed(m, _):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await m.edit_text(_["server_12"])
        test.download()
        await m.edit_text(_["server_13"])
        test.upload()
        test.results.share()
        result = test.results.dict()
        await m.edit_text(_["server_14"])
    except Exception as e:
        return await m.edit_text(f"<code>{e}</code>")
    return result


@app.on_message(
    filters.command(
        ["speedtest", "spt"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
    & SUDOERS
)
@language
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["server_11"])
    result = await testspeed(m, _)  # Directly await the async function
    output = _["server_15"].format(
        result["client"]["isp"],
        result["client"]["country"],
        result["server"]["name"],
        result["server"]["country"],
        result["server"]["cc"],
        result["server"]["sponsor"],
        result["server"]["latency"],
        result["ping"],
    )
    await message.reply_photo(photo=result["share"], caption=output)
    await m.delete()
