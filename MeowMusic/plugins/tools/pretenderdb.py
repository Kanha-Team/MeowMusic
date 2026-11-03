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

impdb = mongo.pretender


async def usr_data(user_id: int) -> bool:
    user = await impdb.find_one({"user_id": user_id})
    return bool(user)


async def get_userdata(user_id: int) -> bool:
    user = await impdb.find_one({"user_id": user_id})
    return user["username"], user["first_name"], user["last_name"]


async def add_userdata(user_id: int, username, first_name, last_name):
    await impdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )


async def check_pretender(chat_id: int) -> bool:
    chat = await impdb.find_one({"chat_id_toggle": chat_id})
    return bool(chat)


async def impo_on(chat_id: int) -> bool:
    was_on = await check_pretender(chat_id)
    if not was_on:
        await impdb.insert_one({"chat_id_toggle": chat_id})
    return was_on


async def impo_off(chat_id: int) -> bool:
    was_on = await check_pretender(chat_id)
    if was_on:
        await impdb.delete_one({"chat_id_toggle": chat_id})
    return was_on
