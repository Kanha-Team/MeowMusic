# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BANNED_USERS
from MeowMusic import app
from MeowMusic.utils.database import get_lang, set_lang
from MeowMusic.utils.decorators import ActualAdminCB, language, languageCB
from strings import get_string, languages_present


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    )
    return keyboard


@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"],
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(_["lang_4"], show_alert=True)
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)
    except:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


REPO_VIDEO = "https://telegra.ph/file/1a3c152717eb9d2e94dc2.mp4"


@app.on_message(filters.command(["repo", "source"]))
async def send_repo(_, message: Message):
    await message.reply_video(
        video=REPO_VIDEO,
        caption=(
            "<blockquote><b>✨ ᴍᴇᴏᴡ ᴍᴜꜱɪᴄ ✨</b>\n\n"
            "🎧 ᴛʜɪꜱ ɪꜱ ᴛʜᴇ ᴏᴘᴇɴ-ꜱᴏᴜʀᴄᴇ ʀᴇᴘᴏꜱɪᴛᴏʀʏ ᴏꜰ ᴛʜᴇ ʙᴏᴛ.\n"
            "⭐ ɪꜰ ʏᴏᴜ ʟɪᴋᴇ ɪᴛ, ɢɪᴠᴇ ᴜꜱ ᴀ ꜱᴛᴀʀ ᴀɴᴅ ꜱʜᴀʀᴇ ɪᴛ ᴡɪᴛʜ ꜰʀɪᴇɴᴅꜱ.\n\n"
            "🧡 ᴄʀᴇᴅɪᴛꜱ : <a href='https://t.me/MeowCloner'>@MeowCloner</a></blockquote>"
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📂 Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ",
                        url="https://github.com/Kanha-Team/MeowMusic/fork",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📂 Mᴜꜱɪᴄ Bᴏᴛ",
                        url="https://github.com/Kanha-Team/KanhaMusic/fork",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🤖 Cʟᴏɴᴇ Bᴏᴛ",
                        url="https://github.com/Kanha-Team/KanhaClone/fork",
                    )
                ],
            ]
        ),
        supports_streaming=True,
        has_spoiler=True,
    )
