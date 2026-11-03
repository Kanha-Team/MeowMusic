# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import sys
import types

try:
    import pyrogram.emoji  # noqa: F401
except ModuleNotFoundError:
    _emoji = types.ModuleType("pyrogram.emoji")
    for _name, _val in {
        "FLAG_BELARUS": "BY",
        "FLAG_CHINA": "CN",
        "FLAG_FRANCE": "FR",
        "FLAG_GERMANY": "DE",
        "FLAG_INDONESIA": "ID",
        "FLAG_ITALY": "IT",
        "FLAG_RUSSIA": "RU",
        "FLAG_SOUTH_KOREA": "KR",
        "FLAG_SPAIN": "ES",
        "FLAG_TURKEY": "TR",
        "FLAG_UKRAINE": "UA",
        "FLAG_UNITED_KINGDOM": "GB",
        "FLAG_UZBEKISTAN": "UZ",
    }.items():
        setattr(_emoji, _name, _val)
    sys.modules["pyrogram.emoji"] = _emoji

from SafoneAPI import SafoneAPI

from MeowMusic.core.bot import Meow
from MeowMusic.core.dir import dirr
from MeowMusic.core.git import git
from MeowMusic.core.userbot import Userbot
from MeowMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Meow()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
