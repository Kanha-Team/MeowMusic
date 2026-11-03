# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from MeowMusic.utils.buttons import btn


def song_markup(_, vidid):
    buttons = [
        [
            btn(text=_["SG_B_2"], callback_data=f"song_helper audio|{vidid}"),
            btn(text=_["SG_B_3"], callback_data=f"song_helper video|{vidid}"),
        ],
        [
            btn(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons
