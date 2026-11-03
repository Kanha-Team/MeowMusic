# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

from config import MONGO_DB_URI

mongo = MongoCli(MONGO_DB_URI).Rankings

nightdb = mongo.nightmode


async def nightmode_on(chat_id: int):
    return nightdb.insert_one({"chat_id": chat_id})


async def nightmode_off(chat_id: int):
    return nightdb.delete_one({"chat_id": chat_id})


async def get_nightchats() -> list:
    chats = nightdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list
