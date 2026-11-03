# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import math

from MeowMusic import app
from MeowMusic.utils.buttons import btn
from MeowMusic.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            btn(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            btn(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)

    remaining_sec = duration_sec - played_sec
    remaining_sec = max(remaining_sec, 0)

    rem_min = remaining_sec // 60
    rem_sec = remaining_sec % 60
    remaining = f"{rem_min:02d}:{rem_sec:02d}"

    percentage = (played_sec / duration_sec) * 100 if duration_sec else 0
    umm = math.floor(percentage)

    if 0 < umm <= 10:
        bar = "|✄—————————|"
    elif 10 < umm < 20:
        bar = "|—✄————————|"
    elif 20 <= umm < 30:
        bar = "|——✄———————|"
    elif 30 <= umm < 40:
        bar = "|———✄——————|"
    elif 40 <= umm < 50:
        bar = "|————✄—————|"
    elif 50 <= umm < 60:
        bar = "|—————✄————|"
    elif 60 <= umm < 70:
        bar = "|——————✄———|"
    elif 70 <= umm < 80:
        bar = "|———————✄——|"
    elif 80 <= umm < 95:
        bar = "|————————✄—|"
    else:
        bar = "|—————————✄|"

    buttons = [
        [
            btn(
                text=f"{played} {bar} {remaining}",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            btn(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            btn(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            btn(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            btn(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
            btn(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            btn(text="-15s", callback_data=f"SEEK seek_backward_15|{chat_id}"),
            btn(text="15s+", callback_data=f"SEEK seek_forward_15|{chat_id}"),
        ],
        [btn(text="ᴄʟᴏsᴇ", callback_data="close")],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            btn(
                text="00:00 |✄—————————| --:--",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            btn(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            btn(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            btn(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            btn(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
            btn(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            btn(text="-15s", callback_data=f"SEEK seek_backward_15|{chat_id}"),
            btn(text="15s+", callback_data=f"SEEK seek_forward_15|{chat_id}"),
        ],
        [btn(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            btn(
                text=_["P_B_1"],
                callback_data=f"KanhaPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
            ),
            btn(
                text=_["P_B_2"],
                callback_data=f"KanhaPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
            ),
        ],
        [
            btn(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            btn(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
            ),
        ],
        [
            btn(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            btn(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            btn(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            btn(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
            btn(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
            ),
            btn(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
            ),
        ],
    ]
    return buttons
