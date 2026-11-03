# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BANNED_USERS, OWNER_ID
from MeowMusic import app

# Fun Actions

SLAP_GIFS = [
    "https://files.catbox.moe/qffez6.mp4",
    "https://files.catbox.moe/7nn58x.mp4",
    "https://files.catbox.moe/afqi54.mp4",
    "https://files.catbox.moe/6z6ncs.mp4",
    "https://files.catbox.moe/q8ox46.mp4",
    "https://files.catbox.moe/r39065.mp4",
    "https://files.catbox.moe/iuzp5f.mp4",
    "https://files.catbox.moe/omjrcd.mp4",
    "https://files.catbox.moe/9rq4j2.mp4",
    "https://files.catbox.moe/7ejq8g.mp4",
    "https://files.catbox.moe/zlu96d.mp4",
    "https://files.catbox.moe/69jrne.mp4",
]

KICK_GIFS = [
    "https://files.catbox.moe/kpmum8.mp4",
    "https://files.catbox.moe/ec7x6p.mp4",
    "https://files.catbox.moe/d5u43d.mp4",
    "https://files.catbox.moe/wl2omf.mp4",
    "https://files.catbox.moe/nzdo3a.mp4",
]

HUG_GIFS = [
    "https://files.catbox.moe/3u911m.mp4",
    "https://files.catbox.moe/0fwjhl.mp4",
    "https://files.catbox.moe/t1sxxn.mp4",
    "https://files.catbox.moe/c6chlr.mp4",
    "https://files.catbox.moe/dyhp3j.mp4",
    "https://files.catbox.moe/oxoi1d.mp4",
    "https://files.catbox.moe/dq2h8n.mp4",
    "https://files.catbox.moe/cprqx6.mp4",
    "https://files.catbox.moe/nijery.mp4",
    "https://files.catbox.moe/egsp9e.mp4",
    "https://files.catbox.moe/y7otcd.mp4",
    "https://files.catbox.moe/9qr86x.mp4",
    "https://files.catbox.moe/lebpdz.mp4",
    "https://files.catbox.moe/mz2kyk.mp4",
    "https://files.catbox.moe/wxts70.mp4",
    "https://files.catbox.moe/n9ru64.mp4",
    "https://files.catbox.moe/cyhub4.mp4",
    "https://files.catbox.moe/axjn9l.mp4",
    "https://files.catbox.moe/8um2s1.mp4",
    "https://files.catbox.moe/np462r.mp4",
]

KISS_GIFS = [
    "https://files.catbox.moe/7j8vwr.mp4",
    "https://files.catbox.moe/dy6bc1.mp4",
    "https://files.catbox.moe/7hkyl5.mp4",
    "https://files.catbox.moe/7jaax5.mp4",
    "https://files.catbox.moe/aqry6s.mp4",
    "https://files.catbox.moe/69nkn1.mp4",
    "https://files.catbox.moe/rmkvl7.mp4",
    "https://files.catbox.moe/26u5sg.mp4",
    "https://files.catbox.moe/z0a8ns.mp4",
    "https://files.catbox.moe/7agl76.mp4",
    "https://files.catbox.moe/b7siss.mp4",
    "https://files.catbox.moe/85jnqh.mp4",
    "https://files.catbox.moe/fbn6y9.mp4",
    "https://files.catbox.moe/msg2pp.mp4",
    "https://files.catbox.moe/plw7a5.mp4",
    "https://files.catbox.moe/xyj344.mp4",
    "https://files.catbox.moe/q0z584.mp4",
    "https://files.catbox.moe/euov26.mp4",
    "https://files.catbox.moe/z04t87.mp4",
    "https://files.catbox.moe/yreuw1.mp4",
    "https://files.catbox.moe/xtoiw9.mp4",
    "https://files.catbox.moe/varz34.mp4",
    "https://files.catbox.moe/rqz6i2.mp4",
    "https://files.catbox.moe/mozues.mp4",
    "https://files.catbox.moe/meok39.mp4",
    "https://files.catbox.moe/eh28w8.mp4",
    "https://files.catbox.moe/03k6hf.mp4",
    "https://files.catbox.moe/e0f17f.mp4",
]

PAT_GIFS = [
    "https://files.catbox.moe/s8c6gu.mp4",
    "https://files.catbox.moe/1dhq9h.mp4",
    "https://files.catbox.moe/ij8s46.mp4",
    "https://files.catbox.moe/p0otd6.mp4",
    "https://files.catbox.moe/gnvg9x.mp4",
    "https://files.catbox.moe/oufbgh.mp4",
    "https://files.catbox.moe/6a39z1.mp4",
    "https://files.catbox.moe/lr6pn3.mp4",
    "https://files.catbox.moe/nrgl0m.mp4",
    "https://files.catbox.moe/kg1rrn.mp4",
    "https://files.catbox.moe/7pj7yp.mp4",
    "https://files.catbox.moe/ucp6z0.mp4",
    "https://files.catbox.moe/g22rvs.mp4",
    "https://files.catbox.moe/kij7ht.mp4",
    "https://files.catbox.moe/o2kd1c.mp4",
    "https://files.catbox.moe/gky4de.mp4",
    "https://files.catbox.moe/s9kpi3.mp4",
    "https://files.catbox.moe/85a3zn.mp4",
    "https://files.catbox.moe/sd7vgl.mp4",
    "https://files.catbox.moe/5j8x81.mp4",
    "https://files.catbox.moe/84v0uk.mp4",
    "https://files.catbox.moe/8oqmwp.mp4",
    "https://files.catbox.moe/soeqrw.mp4",
    "https://files.catbox.moe/po1vg7.mp4",
    "https://files.catbox.moe/hijtnk.mp4",
    "https://files.catbox.moe/kc1vq9.mp4",
    "https://files.catbox.moe/unrx2i.mp4",
    "https://files.catbox.moe/gi565t.mp4",
    "https://files.catbox.moe/oz6ha1.mp4",
    "https://files.catbox.moe/6nps3s.mp4",
    "https://files.catbox.moe/te0rv1.mp4",
    "https://files.catbox.moe/wv5qdm.mp4",
]


# slap a user !
@app.on_message(
    filters.command(["slap"], prefixes=["s", "S", "#"]) & filters.group & ~BANNED_USERS
)
async def slap_handler(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if replied and replied.from_user:
        gif = random.choice(SLAP_GIFS)
        sender = message.from_user.mention
        target_user = replied.from_user
        receiver = target_user.mention

        if target_user.id == OWNER_ID:
            if message.from_user.id == OWNER_ID:
                await message.reply_text(
                    "Bᴏss, ʏᴏᴜ’ʀᴇ ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ — I’ᴍ ʜᴇʀᴇ ᴛᴏ ʀᴇsᴘᴇᴄᴛ, ɴᴏᴛ sʟᴀᴘ!"
                )
                return

            await message.reply_animation(
                gif, caption=f"Sᴛᴇᴘ ʙᴀᴄᴋ, {sender} — ᴍʏ ᴏᴡɴᴇʀ’s ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ! 😎"
            )
            return

        await message.reply_animation(gif, caption=f"{sender} sʟᴀᴘᴘᴇᴅ {receiver} ✨")

    elif len(args) > 1:
        username = args[1].lstrip("@")
        try:
            gif = random.choice(SLAP_GIFS)
            sender = message.from_user.mention
            target = await client.get_users(username)
            receiver = target.mention

            if target.id == OWNER_ID:
                if message.from_user.id == OWNER_ID:
                    await message.reply_text(
                        "Bᴏss, ʏᴏᴜ’ʀᴇ ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ — I’ᴍ ʜᴇʀᴇ ᴛᴏ ʀᴇsᴘᴇᴄᴛ, ɴᴏᴛ sʟᴀᴘ!"
                    )
                    return

                await message.reply_animation(
                    gif, caption=f"Sᴛᴇᴘ ʙᴀᴄᴋ, {sender} — ᴍʏ ᴏᴡɴᴇʀ’s ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ! 😎"
                )
                return

            await message.reply_animation(
                gif, caption=f"{sender} sʟᴀᴘᴘᴇᴅ {receiver} ✨"
            )
        except Exception:
            await message.reply_text("Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ..")

    else:
        await message.reply_text("Tᴇʟʟ ᴍᴇ ᴡʜᴏ ᴛᴏ sʟᴀᴘ! Rᴇᴘʟʏ ᴏʀ ᴛʏᴘᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ!")


# kick a user !
@app.on_message(
    filters.command(["kick"], prefixes=["k", "K", "#"]) & filters.group & ~BANNED_USERS
)
async def kick_handler(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if replied and replied.from_user:
        gif = random.choice(KICK_GIFS)
        sender = message.from_user.mention
        target_user = replied.from_user
        receiver = target_user.mention

        if target_user.id == OWNER_ID:
            if message.from_user.id == OWNER_ID:
                await message.reply_text(
                    "Bᴏss, ʏᴏᴜ’ʀᴇ ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ — I’ᴍ ʜᴇʀᴇ ᴛᴏ ʀᴇsᴘᴇᴄᴛ, ɴᴏᴛ ᴋɪᴄᴋ!"
                )
                return

            await message.reply_animation(
                gif, caption=f"Sᴛᴇᴘ ʙᴀᴄᴋ, {sender} — ᴍʏ ᴏᴡɴᴇʀ’s ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ! 😎"
            )
            return

        await message.reply_animation(gif, caption=f"{sender} ᴋɪᴄᴋᴇᴅ {receiver} ✨")

    elif len(args) > 1:
        username = args[1].lstrip("@")
        try:
            gif = random.choice(KICK_GIFS)
            sender = message.from_user.mention
            target = await client.get_users(username)
            receiver = target.mention

            if target.id == OWNER_ID:
                if message.from_user.id == OWNER_ID:
                    await message.reply_text(
                        "Bᴏss, ʏᴏᴜ’ʀᴇ ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ — I’ᴍ ʜᴇʀᴇ ᴛᴏ ʀᴇsᴘᴇᴄᴛ, ɴᴏᴛ ᴋɪᴄᴋ!"
                    )
                    return

                await message.reply_animation(
                    gif, caption=f"Sᴛᴇᴘ ʙᴀᴄᴋ, {sender} — ᴍʏ ᴏᴡɴᴇʀ’s ᴜɴᴛᴏᴜᴄʜᴀʙʟᴇ! 😎"
                )
                return

            await message.reply_animation(gif, caption=f"{sender} ᴋɪᴄᴋᴇᴅ {receiver} ✨")
        except Exception:
            await message.reply_text("Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ..")

    else:
        await message.reply_text("Tᴇʟʟ ᴍᴇ ᴡʜᴏ ᴛᴏ ᴋɪᴄᴋ! Rᴇᴘʟʏ ᴏʀ ᴛʏᴘᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ!")


# hug a user !
@app.on_message(
    filters.command(["hug"], prefixes=["h", "H", "#"]) & filters.group & ~BANNED_USERS
)
async def hug_handler(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if replied and replied.from_user:
        gif = random.choice(HUG_GIFS)
        sender = message.from_user.mention
        target_user = replied.from_user
        receiver = target_user.mention

        await message.reply_animation(
            gif, caption=f"{sender} ʜᴜɢɢᴇᴅ {receiver} ᴡᴀʀᴍʟʏ... 💗"
        )

    elif len(args) > 1:
        username = args[1].lstrip("@")
        try:
            gif = random.choice(HUG_GIFS)
            sender = message.from_user.mention
            target = await client.get_users(username)
            receiver = target.mention

            await message.reply_animation(
                gif, caption=f"{sender} ʜᴜɢɢᴇᴅ {receiver} ᴡᴀʀᴍʟʏ... 💗"
            )
        except Exception:
            await message.reply_text("Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ..")

    else:
        await message.reply_text("Tᴇʟʟ ᴍᴇ ᴡʜᴏ ᴛᴏ ʜᴜɢ! Rᴇᴘʟʏ ᴏʀ ᴛʏᴘᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ!")


# Kiss a user !
@app.on_message(
    filters.command(["kiss"], prefixes=["k", "K", "#"]) & filters.group & ~BANNED_USERS
)
async def kiss_handler(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if replied and replied.from_user:
        gif = random.choice(KISS_GIFS)
        sender = message.from_user.mention
        target_user = replied.from_user
        receiver = target_user.mention

        await message.reply_animation(gif, caption=f"{sender} ᴋɪssᴇᴅ {receiver}... 💗")

    elif len(args) > 1:
        username = args[1].lstrip("@")
        try:
            gif = random.choice(KISS_GIFS)
            sender = message.from_user.mention
            target = await client.get_users(username)
            receiver = target.mention

            await message.reply_animation(
                gif, caption=f"{sender} ᴋɪssᴇᴅ {receiver}... 💗"
            )
        except Exception:
            await message.reply_text("Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ..")

    else:
        await message.reply_text("Tᴇʟʟ ᴍᴇ ᴡʜᴏ ᴛᴏ ᴋɪss! Rᴇᴘʟʏ ᴏʀ ᴛʏᴘᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ!")


# pat a user !
@app.on_message(
    filters.command(["pat"], prefixes=["p", "P", "#"]) & filters.group & ~BANNED_USERS
)
async def pat_handler(client: Client, message: Message):
    replied = message.reply_to_message
    args = message.text.split()

    if replied and replied.from_user:
        gif = random.choice(PAT_GIFS)
        sender = message.from_user.mention
        target_user = replied.from_user
        receiver = target_user.mention

        await message.reply_animation(
            gif, caption=f"{sender} ᴘᴀᴛᴛᴇᴅ {receiver} ɢᴇɴᴛʟʏ... 💗"
        )

    elif len(args) > 1:
        username = args[1].lstrip("@")
        try:
            gif = random.choice(PAT_GIFS)
            sender = message.from_user.mention
            target = await client.get_users(username)
            receiver = target.mention

            await message.reply_animation(
                gif, caption=f"{sender} ᴘᴀᴛᴛᴇᴅ {receiver} ɢᴇɴᴛʟʏ... 💗"
            )
        except Exception:
            await message.reply_text("Usᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ..")

    else:
        await message.reply_text("Tᴇʟʟ ᴍᴇ ᴡʜᴏ ᴛᴏ ᴘᴀᴛ! Rᴇᴘʟʏ ᴏʀ ᴛʏᴘᴇ ᴀ ᴜsᴇʀɴᴀᴍᴇ!")


# more comming soon
