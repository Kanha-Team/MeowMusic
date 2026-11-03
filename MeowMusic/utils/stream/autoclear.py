# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import os

from config import autoclean


async def auto_clean(popped):
    try:
        rem = popped["file"]
        autoclean.remove(rem)
        count = autoclean.count(rem)
        if count == 0:
            if "vid_" not in rem and "live_" not in rem and "index_" not in rem:
                try:
                    os.remove(rem)
                except:
                    pass
    except:
        pass


async def clean_queue_files(items):
    """Queue ke sab gaano ki files delete karo, queue wipe karne se pehle."""
    for item in list(items or []):
        await auto_clean(item)
