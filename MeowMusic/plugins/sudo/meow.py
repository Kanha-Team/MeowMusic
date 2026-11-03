# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random
import re

from pyrogram import *
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import *
from pyrogram.types import ChatPrivileges

from config import OWNER_ID
from MeowMusic import app
from MeowMusic.misc import SUDOERS
from MeowMusic.utils.database import get_assistant

Kanha_text = [
    "hey please don't disturb me.",
    "who are you",
    "aap kon ho",
    "aap mere owner to nhi lgte ",
    "hey tum mera name kyu le rhe ho meko sone do",
    "ha bolo kya kaam hai ",
    "dekho abhi mai busy hu ",
    "hey i am busy",
    "aapko smj nhi aata kya ",
    "leave me alone",
    "dude what happend",
]

strict_txt = [
    "i can't restrict against my besties",
    "are you serious i am not restrict to my friends",
    "fuck you bsdk k mai apne dosto ko kyu kru",
    "hey stupid admin ",
    "ha ye phele krlo maar lo ek dusre ki gwaand",
    "i can't hi is my closest friend",
    "i love him please don't restict this user try to usertand ",
]

boss_txt = [
    "Arrey Boss Aap Yha 🤩",
    "Hello Master !",
    "Kaise Ho Master ?",
    "Welcome Master !",
    "Darling Tum Yha 🤩",
]

full_promote = [
    "Kaise Ho Master ? Mai Yha Hu !",
    "Aapke Dil Me Master.. 😉",
    "Yess Boss !",
]

bot_leave_txt = [
    "Ok Boss Jaa Rhi Hu Yha Se... 😥",
    "I leaving group TC all 😔",
    "Jaisa Aap Bole !",
]

chk_bot_txt = ["present Boss !", "Present !", "yhi hu"]

banning_txt = ["Starting....", "Jaisa Aap Bolo Sir..."]

protected_chat = ["-1004454485434", "-1004453420360"]
protected_msg = [
    "Tʜɪs ɪs ʏᴏᴜʀ ᴛᴇʀʀɪᴛᴏʀʏ, ᴀɴᴅ I ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜᴀᴛ ʜᴇʀᴇ... ʙᴇᴄᴀᴜsᴇ I ᴅᴏɴ'ᴛ ᴡᴀɴɴᴀ ᴅɪᴇ...",
    "Tʜɪs ɪs ʏᴏᴜʀ ᴛᴇʀʀɪᴛᴏʀʏ, ᴀɴᴅ I ᴄᴀɴ'ᴛ ᴅᴏ ᴛʜᴀᴛ ʜᴇʀᴇ... ʙᴇᴄᴀᴜsᴇ I ᴅᴏɴ'ᴛ ᴡᴀɴɴᴀ ᴅɪᴇ...",
]


ban = ["ban", "boom", "laura"]
unban = ["unban", "gpay"]
mute = ["mute", "silent", "shut", "chup"]
unmute = ["unmute", "speak", "free", "bolne"]
kick = ["kick", "out", "nikaal"]
promote = ["promote", "adminship"]
fullpromote = ["fullpromote", "fulladmin"]
demote = ["demote", "lelo"]
group = ["group"]
channel = ["channel"]
botleave = ["leave", "chale"]
dlt = ["delete", "dlt"]
chk_bot = ["here", "present"]
baning = ["uda", "gift"]
pind = ["pin", "bta"]

# new cmd's
rights = ["rights", "power"]
add_user = ["add", "kidnap", "bulao", "bula"]


# ========================================= #


@app.on_message(
    filters.command(
        ["eow", "anha", "arling", "aby"],
        prefixes=["m", "M", "k", "K", "d", "D", "b", "B"],
    )
    & SUDOERS
)
async def restriction_app(app: Client, message):
    reply = message.reply_to_message
    chat_id = message.chat.id

    cmd = message.text.split(maxsplit=1)

    if len(cmd) == 1:
        return await message.reply(random.choice(Meowkoo_text))

    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply(
                        "OK, Ban kar diya madrchod ko sala Chutiya tha !"
                    )

        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply("Ok, aap bolte hai to unban kar diya")

        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("get lost! bhga diya bhosdi wale ko")

        for muted in data:
            print(f"present {muted}")
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply("muted successfully! Disgusting people.")

        for unmuted in data:
            print(f"present {unmuted}")
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply("Huh, OK, sir!")

        for promoted in data:
            print(f"present {promoted}")
            if promoted in promote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=True,
                        can_delete_messages=True,
                        can_restrict_members=False,
                        can_pin_messages=True,
                        can_promote_members=False,
                        can_manage_chat=True,
                        can_manage_video_chats=True,
                    ),
                )
                await message.reply("promoted !")

        for demoted in data:
            print(f"present {demoted}")
            if demoted in demote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_chat=False,
                        can_manage_video_chats=False,
                    ),
                )
                await message.reply("demoted !")

    # async def your_function():
    for fullpromoted in data:
        print(f"present {fullpromoted}")
        if fullpromoted in fullpromote:
            await app.promote_chat_member(
                chat_id,
                user_id,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            await message.reply("fullpromoted !")

    # leave bot
    for botleaved in data:
        if botleaved in botleave:
            if message.from_user.id != OWNER_ID:
                return await message.reply_text("ʙʜᴀɢ ʙᴇʜᴀɴᴄʜᴏᴅ .")
            else:
                await message.reply_text(random.choice(bot_leave_txt))
                await app.leave_chat(message.chat.id)

    # Deleting the replied message if a trigger word is found
    for delete in data:
        print(f"present {delete}")
        if delete in dlt:
            try:
                await reply.delete()
                await message.delete()
            except Exception as e:
                print(f"Failed to delete the message. Error: {e}")
            return

    # Pin Msg
    for pinned in data:
        print(f"present {pinned}")
        if pinned in pind:
            if reply:
                try:
                    await message.reply("Ohk Baby Kar Rhi...")
                    await reply.pin()
                except Exception as e:
                    print(f"Failed to Pin the message. Error: {e}")
            else:
                await message.reply("Please reply to a message to pin it!")
            return

    # Check Bot Present Or Not
    for check in data:
        print(f"present {check}")
        if check in chk_bot:
            await message.reply(random.choice(chk_bot_txt))

    # BanAll
    for banusers in data:
        print(f"present {banusers}")
        if banusers in baning:
            if message.from_user.id != OWNER_ID:
                return await message.reply_text("Baap Ko Mat Sikha Kya Karna Hai...")
            else:
                if str(chat_id) in protected_chat:
                    await message.reply(random.choice(protected_msg))
                else:
                    await message.reply_text("ꜱᴛᴀʀᴛɪɴɢ ...")

                    bot = await app.get_chat_member(chat_id, app.me.id)
                    bot_permission = bot.privileges.can_restrict_members == True

                    if bot_permission:
                        async for member in app.get_chat_members(chat_id):
                            try:
                                await app.ban_chat_member(chat_id, member.user.id)
                            except Exception:
                                pass
                    else:
                        await message.reply_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛs.")

    # checkRights
    for checkRights in data:
        print(f"present {checkRights}")
        if checkRights in rights:
            if message.from_user.id != OWNER_ID:
                return await message.reply_text("Baap Ko Mat Sikha Kya Karna Hai...")
            else:
                try:
                    member = await app.get_chat_member(chat_id, app.me.id)

                    if member.status == ChatMemberStatus.ADMINISTRATOR:
                        privileges = member.privileges

                        admin_rights = f"""
**ᴍʏ ᴘᴏᴡᴇʀs? ᴛᴀᴋᴇ ᴀ ʟᴏᴏᴋ ~:**
 - ᴄᴀɴ ᴄʜᴀɴɢᴇ ɪɴғᴏ:  {'✅' if privileges.can_change_info else '❌'}
 - ᴄᴀɴ ʙᴀɴ ᴜsᴇʀ's:   {'✅' if privileges.can_restrict_members else '❌'}
 - ᴄᴀɴ ᴅᴇʟᴇᴛᴇ ᴍsɢ's: {'✅' if privileges.can_delete_messages else '❌'}
 - ᴄᴀɴ ɪɴᴠɪᴛᴇ ᴜsᴇʀs: {'✅' if privileges.can_invite_users else '❌'}
 - ᴄᴀɴ ᴍᴀɴᴀɢᴇ ᴠᴄ:    {'✅' if privileges.can_manage_video_chats else '❌'}
 - ᴄᴀɴ ᴘɪɴ ᴍsɢ's:    {'✅' if privileges.can_pin_messages else '❌'}
 - ᴄᴀɴ ᴀᴅᴅ ᴀᴅᴍɪɴ's:  {'✅' if privileges.can_promote_members else '❌'}
"""
                        await message.reply_text(admin_rights)
                    else:
                        await message.reply_text("❌ Bot is not an admin in this chat.")

                except Exception as e:
                    await message.reply_text(f"⚠️ Error: {e!s}")

    # addsomeone
    for addusers in data:
        if addusers in add_user:
            match = re.search(r"@[\w\d_]{5,}", message.text)
            if not match:
                return await message.reply_text(
                    "ᴘʟᴇᴀsᴇ ᴍᴇɴᴛɪᴏɴ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ɪɴ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ."
                )

            username = match.group(0)

            try:
                userbot = await get_assistant(chat_id)
                await userbot.add_chat_members(chat_id, username)
                return await message.reply_text(
                    f"{username} ʜᴀs Jᴏɪɴᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ sᴜᴄᴄᴇssғᴜʟʟʏ."
                )

            except Exception:
                return
