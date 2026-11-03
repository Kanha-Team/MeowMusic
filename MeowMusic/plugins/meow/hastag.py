# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import requests
from bs4 import BeautifulSoup as BSP
from pyrogram import filters

from MeowMusic import app as Meow

url = "https://all-hashtag.com/library/contents/ajax_generator.php"


@Meow.on_message(filters.command("hastag"))
async def hastag(bot, message):
    global content
    try:
        text = message.text.split(" ", 1)[1]
        data = {"keyword": text, "filter": "top"}

        res = requests.post(url, data).text

        content = BSP(res, "html.parser").find("div", {"class": "copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n/hastag python")

    await message.reply_text(
        f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{content}</pre>", quote=True
    )


mod_name = "Hᴀsʜᴛᴀɢ"
help = """
Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.
° /hastag enter word to generate hastag.
°Exᴀᴍᴘʟᴇ:  /hastag python """
