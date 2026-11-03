# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import config
from MeowMusic import app
from MeowMusic.utils.buttons import btn


def start_panel(_):
    buttons = [
        [
            btn(text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"),
            btn(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


SOURCE_URL = "https://github.com/Kanha-Team/MeowMusic"


def private_panel(_):
    buttons = [
        [
            btn(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            btn(text=_["S_B_11"], callback_data="about_open"),
            btn(text="ɪηғσ 皿", callback_data="api_status"),
        ],
        [
            btn(text="ᴘꝛɪᴠᴧᴄʏ", url=SOURCE_URL),
            btn(text="sσυꝛᴄє", url=SOURCE_URL),
        ],
        [
            btn(text=_["S_B_4"], callback_data="help_menu_main", style="danger"),
        ],
    ]
    return buttons
