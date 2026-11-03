# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram.types import InlineKeyboardMarkup

from MeowMusic.utils.buttons import btn


def stats_buttons(_, status):
    not_sudo = [
        btn(
            text=_["SA_B_1"],
            callback_data="TopOverall",
        )
    ]
    sudo = [
        btn(
            text=_["SA_B_2"],
            callback_data="bot_stats_sudo",
        ),
        btn(
            text=_["SA_B_3"],
            callback_data="TopOverall",
        ),
    ]
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [
                btn(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def back_stats_buttons(_):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    text=_["BACK_BUTTON"],
                    callback_data="stats_back",
                ),
                btn(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl
