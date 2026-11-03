# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import random

from pyrogram import enums, filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_CHAT
from MeowMusic import app
from MeowMusic.plugins.bot.start import MEOW_VID
from MeowMusic.plugins.extra.chatbot import get_send_status
from MeowMusic.utils import help_pannel, main_help_panel
from MeowMusic.utils.buttons import btn
from MeowMusic.utils.database import get_lang
from MeowMusic.utils.decorators.language import LanguageStart, languageCB
from MeowMusic.utils.inline.help import music_help_back_markup, private_help_panel
from MeowMusic.utils.stuffs.buttons import BUTTONS
from MeowMusic.utils.stuffs.helper import Helper
from strings import get_string, helpers


@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: app, update: types.Message | types.CallbackQuery):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        # keyboard = help_pannel(_, True)
        keyboard = main_help_panel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
            reply_markup=keyboard,
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        # keyboard = help_pannel(_)
        keyboard = main_help_panel(_)
        await update.reply_photo(
            photo=HELP_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = music_help_back_markup(_)
    if cb == "hb1":
        await CallbackQuery.edit_message_text(
            helpers.HELP_1.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(
            helpers.HELP_2.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(
            helpers.HELP_3.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(
            helpers.HELP_4.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(
            helpers.HELP_5.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(
            helpers.HELP_6.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(
            helpers.HELP_7.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(
            helpers.HELP_8.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(
            helpers.HELP_9.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(
            helpers.HELP_10.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(
            helpers.HELP_11.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(
            helpers.HELP_12.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(
            helpers.HELP_13.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(
            helpers.HELP_14.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(
            helpers.HELP_15.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )
    elif cb == "hb16":
        await CallbackQuery.edit_message_text(
            helpers.HELP_16.format(random.choice(MEOW_VID)), reply_markup=keyboard
        )


@app.on_callback_query(filters.regex("mbot_cb") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(
        Helper.HELP_M.format(random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON),
        parse_mode=enums.ParseMode.HTML,
    )


@app.on_callback_query(filters.regex("managebot123"))
async def on_back_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    language = await get_lang(CallbackQuery.message.chat.id)
    _ = get_string(language)

    keyboard = help_pannel(_, True)
    if cb == "settings_back_helper":
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
            reply_markup=keyboard,
        )


@app.on_callback_query(filters.regex("mplus"))
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    keyboard = InlineKeyboardMarkup([[btn("ʙᴀᴄᴋ", callback_data="mbot_cb")]])

    if cb == "Okieeeeee":
        await CallbackQuery.edit_message_text(
            "`something errors`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN,
        )
        return

    text = getattr(Helper, cb, None)
    if not text:
        await CallbackQuery.answer("Invalid button", show_alert=True)
        return

    text = f"{text}<a href='{random.choice(MEOW_VID)}'>.</a>"

    await CallbackQuery.edit_message_text(
        text, reply_markup=keyboard, parse_mode=enums.ParseMode.HTML
    )


@app.on_callback_query(filters.regex("our_bots_open") & ~BANNED_USERS)
async def ourbots_section(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    # Our Bots content and buttons
    await callback_query.edit_message_caption(
        caption=_["OUR_BOTS_TEXT"],
        reply_markup=InlineKeyboardMarkup(
            [[btn(text=_["BACK_BUTTON"], callback_data="about_open")]]
        ),
    )


@app.on_callback_query(filters.regex("support_open") & ~BANNED_USERS)
async def support_section(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    # Support content and buttons
    await callback_query.edit_message_caption(
        caption=_["SUPPORT_TEXT"].format(random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    btn(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    btn(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
                ],
                [btn(text=_["BACK_BUTTON"], callback_data="settingsback_helper")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("about_open") & ~BANNED_USERS)
async def about_section(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    # About content and buttons
    await callback_query.edit_message_caption(
        caption=_["ABOUT_TEXT"].format(app.mention, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(
            [
                [btn(text=" σᴡηєʀ ", user_id=config.OWNER_ID)],
                [
                    btn(text="sυᴘᴘσʀᴛ", url=config.SUPPORT_CHAT),
                    btn(text="υᴘᴅᴧᴛєs", url=config.SUPPORT_CHANNEL),
                ],
                [btn(text="ʙᴧᴄᴋ", callback_data="settingsback_helper")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("chatbots_help") & ~BANNED_USERS)
async def chatbots_help(client, callback_query):

    if not get_send_status():
        try:
            await callback_query.answer(
                "This feature is currently disabled!", show_alert=True
            )
        except:
            pass
        return

    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    # About content and buttons
    await callback_query.edit_message_caption(
        caption=_["chatbot_help"],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    btn(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    btn(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
                ],
                [btn(text=_["BACK_BUTTON"], callback_data="settingsback_helper")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("help_menu_main") & ~BANNED_USERS)
async def help_menu_open(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    # About content and buttons
    await callback_query.edit_message_caption(
        caption=_["HELP_MENU_TEXT"].format(app.mention, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    btn(text=_["S_B_13"], callback_data="music_help"),
                    btn(text=_["S_B_14"], callback_data="management_help"),
                ],
                [btn(text=_["S_B_16"], callback_data="chatbots_help")],
                [btn(text=_["BACK_BUTTON"], callback_data="settingsback_helper")],
            ]
        ),
    )


@app.on_callback_query(filters.regex("music_help") & ~BANNED_USERS)
async def music_help(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = help_pannel(_, True)

    # About content and buttons
    await callback_query.edit_message_caption(
        caption=_["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
        reply_markup=keyboard,
    )


# --------------------------- management next buttons -------------------------------


@app.on_callback_query(filters.regex("^secondbackmanagement_help$") & ~BANNED_USERS)
async def secondbackmanagement_help(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    await callback_query.edit_message_caption(
        caption=_["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON),
    )


@app.on_callback_query(filters.regex("^thirdmanagement_help$") & ~BANNED_USERS)
async def thirdmanagement_help(client, callback_query):
    await callback_query.answer()
    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    await callback_query.edit_message_caption(
        caption=_["manage_help_page_3"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON_THIRD),
    )


@app.on_callback_query(filters.regex("^nextmanagement_help$") & ~BANNED_USERS)
async def nextmanagement_help(client, callback_query):
    await callback_query.answer()
    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    await callback_query.edit_message_caption(
        caption=_["manage_help_page_2"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON_SECOND),
    )


@app.on_callback_query(filters.regex("management_help") & ~BANNED_USERS)
async def management_help(client, callback_query):
    try:
        await callback_query.answer()
    except:
        pass

    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    await callback_query.edit_message_caption(
        caption=_["help_1"].format(SUPPORT_CHAT, random.choice(MEOW_VID)),
        reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON),
    )
