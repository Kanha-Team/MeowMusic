# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram.types import InlineKeyboardMarkup

from MeowMusic.utils.buttons import btn


def botplaylist_markup(_):
    buttons = [
        [
            btn(
                text=_["PL_B_1"],
                callback_data="get_playlist_playmode",
            ),
        ],
        [
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def top_play_markup(_):
    buttons = [
        [btn(text=_["PL_B_9"], callback_data="SERVERTOP global")],
        [btn(text=_["PL_B_10"], callback_data="SERVERTOP chat")],
        [btn(text=_["PL_B_11"], callback_data="SERVERTOP user")],
        [
            btn(text=_["BACK_BUTTON"], callback_data="get_playmarkup"),
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def get_playlist_markup(_):
    buttons = [
        [
            btn(text=_["P_B_1"], callback_data="play_playlist a"),
            btn(text=_["P_B_2"], callback_data="play_playlist v"),
        ],
        [
            btn(text=_["BACK_BUTTON"], callback_data="home_play"),
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def top_play_markup(_):
    buttons = [
        [btn(text=_["PL_B_9"], callback_data="SERVERTOP Global")],
        [btn(text=_["PL_B_10"], callback_data="SERVERTOP Group")],
        [btn(text=_["PL_B_11"], callback_data="SERVERTOP Personal")],
        [
            btn(text=_["BACK_BUTTON"], callback_data="get_playmarkup"),
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def failed_top_markup(_):
    buttons = [
        [
            btn(
                text=_["BACK_BUTTON"],
                callback_data="get_top_playlists",
            ),
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


def warning_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    text=_["PL_B_7"],
                    callback_data="delete_whole_playlist",
                ),
            ],
            [
                btn(
                    text=_["BACK_BUTTON"],
                    callback_data="del_back_playlist",
                ),
                btn(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ],
        ]
    )
    return upl


def close_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                btn(
                    text=_["CLOSE_BUTTON"],
                    callback_data="close",
                ),
            ]
        ]
    )
    return upl
