# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS
from MeowMusic import YouTube, app
from MeowMusic.core.call import Meow
from MeowMusic.misc import SUDOERS, db
from MeowMusic.utils import AdminRightsCheck, seconds_to_min
from MeowMusic.utils.inline import close_markup


@app.on_message(
    filters.command(["seek", "cseek", "seekback", "cseekback"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def seek_comm(cli, message: Message, _, chat_id):
    if len(message.command) == 1:
        return await message.reply_text(_["admin_20"])
    query = message.text.split(None, 1)[1].strip()
    if not query.isnumeric():
        return await message.reply_text(_["admin_21"])
    playing = db.get(chat_id)
    if not playing:
        return await message.reply_text(_["queue_2"])
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return await message.reply_text(_["admin_22"])
    file_path = playing[0]["file"]
    duration_played = int(playing[0]["played"])
    duration_to_skip = int(query)
    duration = playing[0]["dur"]
    if message.command[0][-2] == "c":
        if (duration_played - duration_to_skip) <= 10:
            return await message.reply_text(
                text=_["admin_23"].format(seconds_to_min(duration_played), duration),
                reply_markup=close_markup(_),
            )
        to_seek = duration_played - duration_to_skip + 1
    else:
        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            return await message.reply_text(
                text=_["admin_23"].format(seconds_to_min(duration_played), duration),
                reply_markup=close_markup(_),
            )
        to_seek = duration_played + duration_to_skip + 1
    mystic = await message.reply_text(_["admin_24"])
    if "vid_" in file_path:
        n, file_path = await YouTube.video(playing[0]["vidid"], True)
        if n == 0:
            return await message.reply_text(_["admin_22"])
    check = (playing[0]).get("speed_path")
    if check:
        file_path = check
    if "index_" in file_path:
        file_path = playing[0]["vidid"]
    try:
        await Meow.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )
    except:
        return await mystic.edit_text(_["admin_26"], reply_markup=close_markup(_))
    if message.command[0][-2] == "c":
        db[chat_id][0]["played"] -= duration_to_skip
    else:
        db[chat_id][0]["played"] += duration_to_skip
    await mystic.edit_text(
        text=_["admin_25"].format(seconds_to_min(to_seek), message.from_user.mention),
        reply_markup=close_markup(_),
    )


# ______[ SEEK AND SEEKBACK CALLBACKS ]________


async def check_callback_admin(client, callback_query: CallbackQuery):
    if callback_query.from_user.id in BANNED_USERS:
        await callback_query.answer(
            "🚫 ʏᴏᴜ'ʀᴇ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜɪs ʙᴏᴛ!", show_alert=True
        )
        return False

    if callback_query.from_user.id in SUDOERS:
        return True

    try:
        chat_id = callback_query.message.chat.id
        member = await app.get_chat_member(chat_id, callback_query.from_user.id)
        if member.privileges and member.privileges.can_manage_video_chats:
            return True
    except Exception as e:
        print(f"Error checking admin status: {e}")

    await callback_query.answer(
        "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴀɴᴀɢᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ's\n\nʀᴇʟᴏᴀᴅ ᴀᴅᴍɪɴs ᴄᴀᴄʜᴇ ᴠɪᴀ : /reload ",
        show_alert=True,
    )
    return False


@app.on_callback_query(filters.regex(r"^SEEK seek_forward_15\|"))
async def seek_forward_15_cb(client, callback_query: CallbackQuery):
    if not await check_callback_admin(client, callback_query):
        return

    try:
        chat_id = int(callback_query.data.split("|")[1])
        playing = db.get(chat_id)

        if not playing:
            await callback_query.answer(
                "ᴛʜᴇ ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ.", show_alert=True
            )
            return

        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            await callback_query.answer("ᴄᴀɴ'ᴛ sᴇᴇᴋ ɪɴ ʟɪᴠᴇ sᴛʀᴇᴀᴍs!", show_alert=True)
            return

        duration_to_skip = 15
        duration_played = int(playing[0]["played"])
        duration = playing[0]["dur"]
        file_path = playing[0]["file"]

        if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
            await callback_query.answer(
                "ᴀʟʀᴇᴀᴅʏ ɴᴇᴀʀ ᴛʜᴇ ᴇɴᴅ ᴏғ ᴛʀᴀᴄᴋ!", show_alert=True
            )
            return

        to_seek = duration_played + duration_to_skip + 1

        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                await callback_query.answer("ᴠɪᴅᴇᴏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ!", show_alert=True)
                return

        check = (playing[0]).get("speed_path")
        if check:
            file_path = check
        if "index_" in file_path:
            file_path = playing[0]["vidid"]

        await Meow.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )

        db[chat_id][0]["played"] += duration_to_skip
        await callback_query.answer("✅ » sᴛʀᴇᴀᴍ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴇᴋᴇᴅ — 15 sᴇᴄᴏɴᴅ's !")

    except Exception as e:
        print(f"Error in seek_forward_15_cb: {e}")
        await callback_query.answer("🚫 ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴇᴋ ғᴏʀᴡᴀʀᴅ!", show_alert=True)


@app.on_callback_query(filters.regex(r"^SEEK seek_backward_15\|"))
async def seek_backward_15_cb(client, callback_query: CallbackQuery):
    if not await check_callback_admin(client, callback_query):
        return

    try:
        chat_id = int(callback_query.data.split("|")[1])
        playing = db.get(chat_id)

        if not playing:
            await callback_query.answer(
                "ᴛʜᴇ ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ.", show_alert=True
            )
            return

        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            await callback_query.answer("ᴄᴀɴ'ᴛ sᴇᴇᴋ ɪɴ ʟɪᴠᴇ sᴛʀᴇᴀᴍ's!", show_alert=True)
            return

        duration_to_skip = 15
        duration_played = int(playing[0]["played"])
        duration = playing[0]["dur"]
        file_path = playing[0]["file"]

        if (duration_played - duration_to_skip) <= 10:
            await callback_query.answer(
                "ᴀʟʀᴇᴀᴅʏ ɴᴇᴀʀ ᴛʜᴇ sᴛᴀʀᴛ ᴏғ ᴛʀᴀᴄᴋ!", show_alert=True
            )
            return

        to_seek = duration_played - duration_to_skip + 1

        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                await callback_query.answer("ᴠɪᴅᴇᴏ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ!", show_alert=True)
                return

        check = (playing[0]).get("speed_path")
        if check:
            file_path = check
        if "index_" in file_path:
            file_path = playing[0]["vidid"]

        await Meow.seek_stream(
            chat_id,
            file_path,
            seconds_to_min(to_seek),
            duration,
            playing[0]["streamtype"],
        )

        db[chat_id][0]["played"] -= duration_to_skip
        await callback_query.answer("✅ sᴛʀᴇᴀᴍ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴇᴋᴇᴅ ʙᴀᴄᴋ 15 sᴇᴄᴏɴᴅ's")

    except Exception as e:
        print(f"Error in seek_backward_15_cb: {e}")
        await callback_query.answer("🚫 ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴇᴋ ʙᴀᴄᴋᴡᴀʀᴅ!", show_alert=True)
