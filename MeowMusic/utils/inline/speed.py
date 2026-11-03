# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram.types import InlineKeyboardMarkup

from MeowMusic.utils.buttons import btn


def speed_markup(_, chat_id):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(text="🕒 0.5x", callback_data=f"SpeedUP {chat_id}|0.5"),
                btn(text="🕓 0.75x", callback_data=f"SpeedUP {chat_id}|0.75"),
            ],
            [
                btn(text=_["P_B_4"], callback_data=f"SpeedUP {chat_id}|1.0"),
            ],
            [
                btn(text="🕤 1.5x", callback_data=f"SpeedUP {chat_id}|1.5"),
                btn(text="🕛 2.0x", callback_data=f"SpeedUP {chat_id}|2.0"),
            ],
            [
                btn(text=_["CLOSE_BUTTON"], callback_data="close"),
            ],
        ]
    )
    return upl
