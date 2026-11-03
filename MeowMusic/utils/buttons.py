# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram.types import InlineKeyboardButton

import config

try:
    from pyrogram.enums import ButtonStyle
except ImportError:
    ButtonStyle = None

_COLOUR_MAP = {}
if ButtonStyle is not None:
    _COLOUR_MAP = {
        "danger": ButtonStyle.DANGER,
        "red": ButtonStyle.DANGER,
        "primary": ButtonStyle.PRIMARY,
        "blue": ButtonStyle.PRIMARY,
        "success": ButtonStyle.SUCCESS,
        "green": ButtonStyle.SUCCESS,
    }

_COLOURS = list(dict.fromkeys(_COLOUR_MAP.values()))


def random_style():
    return random.choice(_COLOURS) if _COLOURS else None


def btn(text, style=None, icon=None, **kw):
    if config.DISABLE_COLOUR or not _COLOURS:
        return InlineKeyboardButton(text=text, **kw)
    chosen = _COLOUR_MAP.get(str(style).lower()) if style is not None else None
    if chosen is None:
        chosen = random.choice(_COLOURS)
    try:
        return InlineKeyboardButton(text=text, style=chosen, **kw)
    except (TypeError, AttributeError):
        return InlineKeyboardButton(text=text, **kw)
