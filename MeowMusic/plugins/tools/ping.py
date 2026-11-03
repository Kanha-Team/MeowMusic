# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from config import *
from config import BANNED_USERS
from MeowMusic import app
from MeowMusic.core.call import Meow
from MeowMusic.utils import bot_sys_stats
from MeowMusic.utils.database import command_lock_check
from MeowMusic.utils.decorators.language import language
from MeowMusic.utils.inline import supp_markup


@app.on_message(
    filters.command("ping", prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
    & command_lock_check()
    & ~BANNED_USERS
)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo="https://i.ibb.co/VWnm6f3f/ping.jpg",
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Meow.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
