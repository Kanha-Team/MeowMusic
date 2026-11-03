# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram.types import InlineKeyboardMarkup

from MeowMusic import app
from MeowMusic.utils.buttons import btn


def help_pannel(_, START: bool | int | None = None):
    first = [btn(text=_["CLOSE_BUTTON"], callback_data="close")]
    second = [btn(text=_["BACK_BUTTON"], callback_data="help_menu_main")]
    mark = second if START else first
    upl = InlineKeyboardMarkup(
        [
            [
                btn(text=_["H_B_1"], callback_data="help_callback hb1"),
                btn(text=_["H_B_2"], callback_data="help_callback hb2"),
                btn(text=_["H_B_3"], callback_data="help_callback hb3"),
            ],
            [
                btn(text=_["H_B_4"], callback_data="help_callback hb4"),
                btn(text=_["H_B_5"], callback_data="help_callback hb5"),
                btn(text=_["H_B_6"], callback_data="help_callback hb6"),
            ],
            [
                btn(text=_["H_B_7"], callback_data="help_callback hb7"),
                btn(text=_["H_B_8"], callback_data="help_callback hb8"),
                btn(text=_["H_B_13"], callback_data="help_callback hb13"),
            ],
            [
                btn(text=_["H_B_11"], callback_data="help_callback hb11"),
                btn(text=_["H_B_14"], callback_data="help_callback hb14"),
                btn(text=_["H_B_10"], callback_data="help_callback hb10"),
            ],
            [
                btn(text=_["H_B_12"], callback_data="help_callback hb12"),
                btn(text=_["PL_B_0"], callback_data="help_callback hb16"),
                btn(text=_["H_B_15"], callback_data="help_callback hb15"),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def music_help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    text=_["BACK_BUTTON"],
                    callback_data="music_help",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            btn(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons


def main_help_panel(_, START: bool | int | None = None):
    [btn(text=_["CLOSE_BUTTON"], callback_data="close")]
    [btn(text=_["BACK_BUTTON"], callback_data="help_menu_main")]
    upl = InlineKeyboardMarkup(
        [
            [
                btn(text=_["S_B_13"], callback_data="music_help"),
                btn(text=_["S_B_14"], callback_data="management_help"),
            ],
            [btn(text=_["S_B_16"], callback_data="chatbots_help")],
            [btn(text=_["BACK_BUTTON"], callback_data="settingsback_helper")],
        ]
    )
    return upl
