# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from MeowMusic import LOGGER, app, userbot
from MeowMusic.core.call import Meow
from MeowMusic.misc import sudo
from MeowMusic.plugins import ALL_MODULES
from MeowMusic.utils.database import get_banned_users, get_gbanned


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        sys.exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("MeowMusic.plugins" + all_module)
    LOGGER("MeowMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Meow.start()
    try:
        await Meow.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("MeowMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        sys.exit()
    except:
        pass
    await Meow.decorators()
    LOGGER("MeowMusic").info(
        "\x4d\x65\x6f\x77\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x65\x79\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x46\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x4d\x65\x6f\x77\x43\x6c\x6f\x6e\x65\x72"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("MeowMusic").info("Stopping 𝐓‌ʜє 𝐌‌єσᴡ 🚩𝐓‌єᴧϻ Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
