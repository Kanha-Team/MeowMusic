# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


import requests
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL

from config import BANNED_USERS, OWNER_ID
from MeowMusic import app
from MeowMusic.core.mongo import mongodb
from MeowMusic.utils.database import get_lang, is_command_locked
from MeowMusic.utils.decorators.language import language, languageCB
from MeowMusic.utils.inline.playlist import (
    botplaylist_markup,
    get_playlist_markup,
    warning_markup,
)
from MeowMusic.utils.stream.stream import stream
from strings import get_string

SERVER_PLAYLIST_LIMIT = 50


playlistdb = mongodb.playlist
playlist = []


async def _get_playlists(chat_id: int) -> dict[str, int]:
    _notes = await playlistdb.find_one({"chat_id": chat_id})
    if not _notes:
        return {}
    return _notes["notes"]


async def get_playlist_names(chat_id: int) -> list[str]:
    _notes = []
    for note in await _get_playlists(chat_id):
        _notes.append(note)
    return _notes


async def get_playlist(chat_id: int, name: str) -> bool | dict:
    name = name
    _notes = await _get_playlists(chat_id)
    if name in _notes:
        return _notes[name]
    else:
        return False


async def save_playlist(chat_id: int, name: str, note: dict):
    name = name
    _notes = await _get_playlists(chat_id)
    _notes[name] = note
    await playlistdb.update_one(
        {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
    )


async def delete_playlist(chat_id: int, name: str) -> bool:
    notesd = await _get_playlists(chat_id)
    name = name
    if name in notesd:
        del notesd[name]
        await playlistdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"notes": notesd}},
            upsert=True,
        )
        return True
    return False


async def update_playlist(chat_id: int, name: str, note: dict):
    """
    Update the playlist with the given name and note for the specific chat_id.
    """
    _notes = await _get_playlists(chat_id)

    if name in _notes:
        _notes[name] = note
        await playlistdb.update_one(
            {"chat_id": chat_id}, {"$set": {"notes": _notes}}, upsert=True
        )
        return True
    return False


ADDPLAYLIST_COMMAND = "addsong"
PLAYLIST_COMMAND = "playlist"
DELETESONG_COMMAND = "delsong"


PAGE_SIZE = 15  # Number of songs per page in expanded mode
COLLAPSE_SIZE = 5  # Number of songs per page in collapsed mode
expanded_users = set()  # Keeps track of users who expanded their playlist


@app.on_message(
    filters.command(["playlist", "plist"], prefixes=["/", "!", "."]) & ~BANNED_USERS
)
@language
async def check_playlist(client, message: Message, _):

    if await is_command_locked(message.chat.id, "playlist"):
        return

    user_id = message.from_user.id
    _playlist = await get_playlist_names(user_id)

    if not _playlist:
        return await message.reply_text(_["playlist_3"])

    is_expanded = user_id in expanded_users
    await send_playlist_page(client, message, user_id, 1, is_expanded, is_home=True)


async def send_playlist_page(client, event, user_id, page, is_expanded, is_home=False):
    """Sends or updates the playlist page with navigation buttons and expansion/collapse state."""
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        return (
            await event.message.edit_text("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ.")
            if isinstance(event, CallbackQuery)
            else await event.reply_text("ʏᴏᴜ ʜᴀᴠᴇ ɴᴏ ᴘʟᴀʏʟɪsᴛ.")
        )

    total_songs = len(_playlist)
    songs_per_page = PAGE_SIZE if is_expanded else COLLAPSE_SIZE
    start, end = (page - 1) * songs_per_page, page * songs_per_page
    current_songs = _playlist[start:end]

    title = f"◆ {event.from_user.first_name}'s {'ғᴜʟʟ ' if is_expanded else ''}ᴘʟᴀʏʟɪsᴛ (Page {page}). \n◆ <b>ᴛᴏᴛᴀʟ sᴏɴɢs: {total_songs}</b>"
    msg = f"<blockquote>{title}</blockquote>\n\n<blockquote>"

    for idx, song in enumerate(current_songs, start=start + 1):
        _note = await get_playlist(user_id, song)
        msg += f"{idx}. {_note['title'].title()}\n"
    msg += "</blockquote>"

    keyboard = []
    nav_buttons = []

    # Ensure Previous and Next buttons always appear
    if start > 0:
        nav_buttons.append(
            InlineKeyboardButton(
                "ʙᴀᴄᴋ", callback_data=f"playlist_page|{user_id}|{page-1}"
            )
        )
    if end < total_songs:
        nav_buttons.append(
            InlineKeyboardButton(
                "ɴᴇxᴛ", callback_data=f"playlist_page|{user_id}|{page+1}"
            )
        )

    if is_expanded:
        keyboard.append(
            [
                InlineKeyboardButton(
                    "ᴄᴏʟʟᴀᴘsᴇ", callback_data=f"collapse_playlist_{user_id}"
                )
            ]
        )
    else:
        if total_songs > COLLAPSE_SIZE:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        "ᴇxᴘᴀɴᴅ", callback_data=f"expand_playlist_{user_id}"
                    )
                ]
            )

    if nav_buttons:
        keyboard.append(nav_buttons)

    if nav_buttons and not is_home:
        keyboard.append(
            [InlineKeyboardButton("ʜᴏᴍᴇ", callback_data=f"playlist_home|{user_id}")]
        )

    keyboard.append([InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if isinstance(event, CallbackQuery):
        await event.message.edit_text(msg, reply_markup=reply_markup)
    else:
        await event.reply_text(msg, reply_markup=reply_markup)


@app.on_callback_query(filters.regex(r"expand_playlist_(\d+)"))
async def expand_playlist(client, callback_query: CallbackQuery):
    """Expands the playlist and applies it to all pages."""
    user_id = int(callback_query.data.split("_")[-1])

    if user_id != callback_query.from_user.id:
        return await callback_query.answer(
            "ɪᴛ's ɴᴏᴛ ʏᴏᴜʀ ǫᴜᴇʀʏ, ɴᴏʀ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", show_alert=True
        )

    expanded_users.add(user_id)  # Mark user as expanded
    await send_playlist_page(
        client, callback_query, user_id, 1, is_expanded=True, is_home=True
    )


@app.on_callback_query(filters.regex(r"collapse_playlist_(\d+)"))
async def collapse_playlist(client, callback_query: CallbackQuery):
    """Collapses the playlist and applies it to all pages."""
    user_id = int(callback_query.data.split("_")[-1])

    if user_id != callback_query.from_user.id:
        return await callback_query.answer(
            "ɪᴛ's ɴᴏᴛ ʏᴏᴜʀ ǫᴜᴇʀʏ, ɴᴏʀ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", show_alert=True
        )

    expanded_users.discard(user_id)  # Remove user from expanded list
    await send_playlist_page(
        client, callback_query, user_id, 1, is_expanded=False, is_home=True
    )


@app.on_callback_query(filters.regex(r"playlist_page\|(\d+)\|(\d+)"))
async def paginate_playlist(client, callback_query: CallbackQuery):
    """Handles playlist pagination when user clicks 'Next' or 'Previous'."""
    user_id, page = map(int, callback_query.data.split("|")[1:])

    if user_id != callback_query.from_user.id:
        return await callback_query.answer(
            "ɪᴛ's ɴᴏᴛ ʏᴏᴜʀ ǫᴜᴇʀʏ, ɴᴏʀ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", show_alert=True
        )

    is_expanded = user_id in expanded_users
    await send_playlist_page(client, callback_query, user_id, page, is_expanded)


@app.on_callback_query(filters.regex(r"playlist_home\|(\d+)"))
async def return_to_home(client, callback_query: CallbackQuery):
    """Returns the user to the first page of the playlist."""
    user_id = int(callback_query.data.split("|")[1])

    if user_id != callback_query.from_user.id:
        return await callback_query.answer(
            "ɪᴛ's ɴᴏᴛ ʏᴏᴜʀ ǫᴜᴇʀʏ, ɴᴏʀ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", show_alert=True
        )

    is_expanded = user_id in expanded_users
    await send_playlist_page(
        client, callback_query, user_id, 1, is_expanded, is_home=True
    )


@app.on_message(
    filters.command(["delsong", "rmsong"], prefixes=["/", "!", "."]) & ~BANNED_USERS
)
@language
async def del_plist_msg(client, message: Message, _):
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text(_["playlist_2"])
    else:
        return await message.reply_text(_["playlist_3"])
    keyboard, count = await get_keyboard(_, message.from_user.id)
    await get.edit_text(_["playlist_7"].format(count), reply_markup=keyboard)


# from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

MAX_PER_PAGE = 10  # Max rows per page


async def get_keyboard(_, user_id, page=1):
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)

    start = (page - 1) * MAX_PER_PAGE
    end = start + MAX_PER_PAGE

    current_page_songs = _playlist[start:end]
    (len(_playlist) + MAX_PER_PAGE - 1) // MAX_PER_PAGE

    keyboard = []

    # Add one button per row
    for x in current_page_songs:
        _note = await get_playlist(user_id, x)
        title = _note["title"].title()

        keyboard.append(
            [InlineKeyboardButton(text=title, callback_data=f"del_playlist {x}")]
        )

    # Pagination buttons (if needed)
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            InlineKeyboardButton("< ᴘʀᴇᴠ", callback_data=f"plist_page {page - 1}")
        )
    if end < len(_playlist):
        nav_buttons.append(
            InlineKeyboardButton("ɴᴇxᴛ >", callback_data=f"plist_page {page + 1}")
        )
    if nav_buttons:
        keyboard.append(nav_buttons)

    # Final row: Delete All + Close
    keyboard.append(
        [
            InlineKeyboardButton(text=_["PL_B_5"], callback_data="delete_warning"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
        ]
    )

    return InlineKeyboardMarkup(keyboard), count


@app.on_callback_query(filters.regex(r"plist_page (\d+)") & ~BANNED_USERS)
async def paginate_playlist(client, callback_query):
    page = int(callback_query.data.split()[1])
    chat_id = callback_query.message.chat.id
    language = await get_lang(chat_id)
    _ = get_string(language)

    keyboard, count = await get_keyboard(_, callback_query.from_user.id, page=page)

    try:
        await callback_query.edit_message_text(
            _["playlist_7"].format(count), reply_markup=keyboard
        )
    except Exception as e:
        print(e)


@app.on_callback_query(filters.regex("play_playlist") & ~BANNED_USERS)
@languageCB
async def play_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await CallbackQuery.answer(
                _["playlist_3"],
                show_alert=True,
            )
        except:
            return
    chat_id = CallbackQuery.message.chat.id
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    result = []
    try:
        await CallbackQuery.answer()
    except:
        pass
    video = True if mode == "v" else None
    mystic = await CallbackQuery.message.reply_text(_["play_1"])
    for vidids in _playlist:
        result.append(vidids)
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_message(
    filters.command(
        ["playplaylist", ("playplist" "pplist"), "pplay"], prefixes=["/", "", "!", "."]
    )
    & ~BANNED_USERS
)
@languageCB
async def play_playlist_command(client, message, _):

    if await is_command_locked(message.chat.id, "playplaylist"):
        return

    mode = message.command[1] if len(message.command) > 1 else None
    user_id = message.from_user.id
    _playlist = await get_playlist_names(user_id)

    if not _playlist:
        try:
            return await message.reply(
                _["playlist_3"],
                quote=True,
            )
        except:
            return

    chat_id = message.chat.id
    user_name = message.from_user.first_name

    try:
        await message.delete()
    except:
        pass

    result = []
    video = True if mode == "v" else None

    mystic = await message.reply_text(_["play_1"])

    for vidids in _playlist:
        result.append(vidids)

    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)

    return await mystic.delete()


@app.on_message(
    filters.command(["addsong", "addplay"], prefixes=["/", "!", "."]) & ~BANNED_USERS
)
@language
async def add_playlist(client, message: Message, _):

    if await is_command_locked(message.chat.id, "addsong"):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ ᴏʀ sᴏɴɢ ʟɪɴᴋ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ᴘʟᴀʏʟɪsᴛ ʟɪɴᴋ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ..."
        )

    query = message.command[1]

    if "youtube.com/playlist" in query:
        adding = await message.reply_text("ᴀᴅᴅɪɴɢ sᴏɴɢs ғʀᴏᴍ ᴘʟᴀʏʟɪsᴛ...")

        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                entries = info.get("entries", [])

                if not entries:
                    return await message.reply_text("ɴᴏ sᴏɴɢs ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴘʟᴀʏʟɪsᴛ.")

                user_id = message.from_user.id

                for entry in entries:
                    video_id = entry.get("id")
                    title = entry.get("title")
                    duration = entry.get("duration")

                    if not all([video_id, title, duration]):
                        continue  # skip if missing info

                    # ✅ Skip if already in playlist
                    _check = await get_playlist(user_id, video_id)
                    if _check:
                        continue

                    plist = {
                        "videoid": video_id,
                        "title": title,
                        "duration": duration,
                    }

                    await save_playlist(user_id, video_id, plist)

                keyboardes = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ sᴏɴɢ?",
                                callback_data=f"open_playlist {user_id}",
                            )
                        ]
                    ]
                )

                await adding.delete()
                return await message.reply_text(
                    "✅ ᴀʟʟ sᴏɴɢs ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ғʀᴏᴍ ᴘʟᴀʏʟɪꜱᴛ!",
                    reply_markup=keyboardes,
                )

        except Exception as e:
            await adding.delete()
            return await message.reply_text(f"ᴇʀʀᴏʀ : {e}")

    if (
        "youtube.com/@" in query
        or "youtube.com/channel/" in query
        or "youtube.com/c/" in query
    ):
        addin = await message.reply_text("ᴀᴅᴅɪɴɢ sᴏɴɢs ғʀᴏᴍ ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ...")

        try:

            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
            }

            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"{query}/videos", download=False)
                entries = info.get("entries", [])

                if not entries:
                    return await message.reply_text(
                        "ɴᴏ sᴏɴɢs ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ."
                    )

                user_id = message.from_user.id

                for entry in entries:
                    video_id = entry.get("id")
                    title = entry.get("title")
                    duration = entry.get("duration")

                    if not all([video_id, title, duration]):
                        continue

                    # ✅ Skip if already in playlist
                    _check = await get_playlist(user_id, video_id)
                    if _check:
                        continue

                    plist = {
                        "videoid": video_id,
                        "title": title,
                        "duration": duration,
                    }

                    await save_playlist(user_id, video_id, plist)

                keyboardes = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "ᴡᴀɴᴛ ʀᴇᴍᴏᴠᴇ sᴏɴɢ?",
                                callback_data=f"open_playlist {user_id}",
                            )
                        ]
                    ]
                )

                await addin.delete()
                return await message.reply_text(
                    "✅ ᴀʟʟ sᴏɴɢs ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ғʀᴏᴍ ʏᴏᴜʀ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ!",
                    reply_markup=keyboardes,
                )

        except Exception as e:
            await addin.delete()
            return await message.reply_text(f"ᴇʀʀᴏʀ : {e}")

    if "youtu" in query:
        try:
            user_id = message.from_user.id

            # ✨ Extract video ID from any YouTube URL
            import re

            pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
            match = re.search(pattern, query)
            if not match:
                return await message.reply_text("ᴄᴏᴜʟᴅ ɴᴏᴛ ᴇxᴛʀᴀᴄᴛ ᴠɪᴅᴇᴏ ID.")
            videoid = match.group(1)

            # 💖 Use your existing MeowMusic.YouTube.details method
            from MeowMusic import YouTube

            title, duration_min, _, _, _ = await YouTube.details(videoid, True)
            title = (title[:50]).title()

            thumbnail = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
            _check = await get_playlist(user_id, videoid)
            if _check:
                return await message.reply_photo(
                    thumbnail, caption="ᴛʜɪs ᴛʀᴀᴄᴋ ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ."
                )

            _count = await get_playlist_names(user_id)
            if len(_count) >= SERVER_PLAYLIST_LIMIT:
                return await message.reply_text(
                    _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                )

            plist = {
                "videoid": videoid,
                "title": title,
                "duration": duration_min,
            }

            await save_playlist(user_id, videoid, plist)

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴘʟᴀʏʟɪsᴛ",
                            callback_data=f"remove_playlist {videoid}",
                        )
                    ]
                ]
            )

            return await message.reply_photo(
                thumbnail, caption="ᴀᴅᴅᴇᴅ sᴏɴɢ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ.", reply_markup=keyboard
            )

        except Exception as e:
            return await message.reply_text(f"ᴇʀʀᴏʀ: {e}")

    else:
        from MeowMusic import YouTube

        query = " ".join(message.command[1:])
        print(query)

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            videoid = results[0]["id"]
            results[0]["views"]
            results[0]["channel"]

            user_id = message.from_user.id
            _check = await get_playlist(user_id, videoid)
            if _check:
                try:
                    return await message.reply_photo(thumbnail, caption=_["playlist_8"])
                except KeyError:
                    pass

            _count = await get_playlist_names(user_id)
            count = len(_count)
            if count == SERVER_PLAYLIST_LIMIT:
                try:
                    return await message.reply_text(
                        _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                    )
                except KeyError:
                    pass

            m = await message.reply("ᴀᴅᴅɪɴɢ sᴏɴɢ...")
            title, duration_min, _, _, _ = await YouTube.details(videoid, True)
            title = (title[:50]).title()
            plist = {
                "videoid": videoid,
                "title": title,
                "duration": duration_min,
            }

            await save_playlist(user_id, videoid, plist)

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴘʟᴀʏʟɪsᴛ",
                            callback_data=f"remove_playlist {videoid}",
                        )
                    ]
                ]
            )
            await m.delete()
            await message.reply_photo(
                thumbnail,
                caption="ᴀᴅᴅᴇᴅ sᴏɴɢ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ...",
                reply_markup=keyboard,
            )

        except KeyError:
            return await message.reply_text("ɪɴᴠᴀʟɪᴅ ᴅᴀᴛᴀ ғᴏʀᴍᴀᴛ ʀᴇᴄᴇɪᴠᴇᴅ.")
        except Exception:
            pass


@app.on_callback_query(filters.regex("open_playlist") & ~BANNED_USERS)
@languageCB
async def open_playlist(client, CallbackQuery, _):
    _playlist = await get_playlist_names(CallbackQuery.from_user.id)
    if _playlist:
        get = await CallbackQuery.message.edit_text(_["playlist_2"])
    else:
        return await CallbackQuery.message.edit_text(_["playlist_3"])
    keyboard, count = await get_keyboard(_, CallbackQuery.from_user.id)
    await get.edit_text(_["playlist_7"].format(count), reply_markup=keyboard)


@app.on_callback_query(filters.regex("remove_playlist") & ~BANNED_USERS)
@languageCB
async def del_plist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    deleted = await delete_playlist(CallbackQuery.from_user.id, videoid)
    if deleted:
        try:
            await CallbackQuery.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await CallbackQuery.answer(_["playlist_12"], show_alert=True)
        except:
            return
    keyboards = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "ʀᴇᴄᴏᴠᴇʀ sᴏɴɢ", callback_data=f"recover_playlist {videoid}"
                )
            ]
        ]
    )
    return await CallbackQuery.edit_message_text(
        text="ʏᴏᴜʀ sᴏɴɢ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴘʟᴀʏʟɪsᴛ...", reply_markup=keyboards
    )


@app.on_callback_query(filters.regex("recover_playlist") & ~BANNED_USERS)
@languageCB
async def add_playlist(client, CallbackQuery, _):
    from MeowMusic import YouTube

    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await CallbackQuery.answer(_["playlist_8"], show_alert=True)
        except:
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await CallbackQuery.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        _duration_sec,
        _thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        keyboardss = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ʀᴇᴍᴏᴠᴇ ᴀɢᴀɪɴ", callback_data=f"remove_playlist {videoid}"
                    )
                ]
            ]
        )
        return await CallbackQuery.edit_message_text(
            text="ʀᴇᴄᴏᴠᴇʀᴇᴅ sᴏɴɢ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ...", reply_markup=keyboardss
        )
    except:
        return


@app.on_callback_query(filters.regex("add_playlist") & ~BANNED_USERS)
@languageCB
async def add_playlist(client, CallbackQuery, _):
    await CallbackQuery.answer(
        "ᴛᴏ ᴀᴅᴅ ᴀ sᴏɴɢ ɪɴ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ ᴊᴜsᴛ ᴛʏᴘᴇ /addplaylist 'song name'",
        show_alert=True,
    )


@app.on_callback_query(filters.regex("PRO_playlist") & ~BANNED_USERS)
@languageCB
async def add_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            from MeowMusic import YouTube

            return await CallbackQuery.answer(_["playlist_8"], show_alert=True)
        except:
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await CallbackQuery.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        _duration_sec,
        _thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await CallbackQuery.answer(
            _["playlist_10"].format(title), show_alert=True
        )
    except:
        return


DELETE_ALL_PLAYLIST_COMMAND = "delplaylist"


@app.on_message(
    filters.command(["delplaylist", ("rmplaylist" "rmplist")], prefixes=["/", "!", "."])
    & ~BANNED_USERS
)
@language
async def delete_all_playlists(client, message, _):

    if await is_command_locked(message.chat.id, "delplaylist"):
        return

    user_id = message.from_user.id
    _playlist = await get_playlist_names(user_id)
    if _playlist:
        try:
            upl = warning_markup(_)
            await message.reply_text(_["playlist_14"], reply_markup=upl)
        except:
            pass
    else:
        await message.reply_text(_["playlist_3"])


@app.on_callback_query(filters.regex("del_playlist") & ~BANNED_USERS)
@languageCB
async def del_plist(client, CallbackQuery, _):

    callback_data = CallbackQuery.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = CallbackQuery.from_user.id
    deleted = await delete_playlist(CallbackQuery.from_user.id, videoid)
    if deleted:
        try:
            await CallbackQuery.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await CallbackQuery.answer(_["playlist_12"], show_alert=True)
        except:
            return
    keyboard, _count = await get_keyboard(_, user_id)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("delete_whole_playlist") & ~BANNED_USERS)
@languageCB
async def del_whole_playlist(client, CallbackQuery, _):

    await CallbackQuery.answer(
        "ᴏᴋ ᴡᴀɪᴛ...\n\nᴅᴇʟᴇᴛɪɴɢ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ...", show_alert=True
    )
    _playlist = await get_playlist_names(CallbackQuery.from_user.id)
    for x in _playlist:
        await delete_playlist(CallbackQuery.from_user.id, x)

    return await CallbackQuery.edit_message_text(_["playlist_13"])


@app.on_callback_query(filters.regex("get_playlist_playmode") & ~BANNED_USERS)
@languageCB
async def get_playlist_playmode_(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    buttons = get_playlist_markup(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("delete_warning") & ~BANNED_USERS)
@languageCB
async def delete_warning_message(client, CallbackQuery, _):

    try:
        await CallbackQuery.answer()
    except:
        pass
    upl = warning_markup(_)
    return await CallbackQuery.edit_message_text(_["playlist_14"], reply_markup=upl)


@app.on_callback_query(filters.regex("home_play") & ~BANNED_USERS)
@languageCB
async def home_play_(client, CallbackQuery, _):

    try:
        await CallbackQuery.answer()
    except:
        pass
    buttons = botplaylist_markup(_)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("del_back_playlist") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):

    user_id = CallbackQuery.from_user.id
    _playlist = await get_playlist_names(user_id)
    if _playlist:
        try:
            await CallbackQuery.answer(_["playlist_2"], show_alert=True)
        except:
            pass
    else:
        try:
            return await CallbackQuery.answer(_["playlist_3"], show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(_, user_id)
    return await CallbackQuery.edit_message_text(
        _["playlist_7"].format(count), reply_markup=keyboard
    )


@app.on_message(filters.command("pstats") & filters.user(OWNER_ID))
async def total_stats(client, message: Message):
    total_users = 0
    total_playlists = 0
    total_deleted = 0
    total_songs = 0
    total_cloned_songs = 0
    total_cloned_playlists = 0
    total_clones = 0
    async for data in playlistdb.find():
        total_users += 1
        user_playlists = data.get("notes", {})
        total_playlists += len(user_playlists)
        total_deleted += data.get("deleted_count", 0)

        for playlist_data in user_playlists.values():
            songs = playlist_data.get("songs", [])
            total_songs += len(songs)

            if playlist_data.get("is_cloned", False):
                total_cloned_songs += len(songs)
                total_cloned_playlists += 1
                total_clones += playlist_data.get(
                    "clone_count", 0
                )  # Track clones per playlist

    stats_message = (
        f"**ᴘʟᴀʏʟɪsᴛ sᴛᴀᴛs**\n\n"
        f"• **ᴘʟᴀʏʟɪsᴛs :** {total_users}\n"
        f"• **ᴛᴏᴛᴀʟ sᴏɴɢs :** {total_playlists}\n"
    )

    await message.reply_text(stats_message)


@app.on_message(
    filters.command(["cloneplaylist", "cloneplist"], prefixes=["/", "!", "."])
    & ~BANNED_USERS
)
@language
async def clone_playlist(client, message: Message, _):

    if await is_command_locked(message.chat.id, "cloneplaylist"):
        return

    """
    if not message.reply_to_message or not message.reply_to_message.from_user:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴛᴏ ᴄʟᴏɴᴇ ᴛʜᴇɪʀ ᴘʟᴀʏʟɪsᴛ.")

    target_user_id = message.reply_to_message.from_user.id
    user_id = message.from_user.id
    """

    user_id = message.from_user.id
    # Case 1: If replied to a user
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user_id = message.reply_to_message.from_user.id

    # Case 2: If user_id or username is passed in command
    elif len(message.command) > 1:
        input_arg = message.command[1]
        if input_arg.startswith("@"):
            try:
                user = await client.get_users(input_arg)
                target_user_id = user.id
            except Exception:
                return await message.reply_text("❌ ᴄᴏᴜʟᴅ ɴᴏᴛ ғɪɴᴅ ᴛʜᴇ ᴜsᴇʀ.")
        else:
            try:
                target_user_id = int(input_arg)
            except ValueError:
                return await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ.")
    else:
        return await message.reply_text(
            "⚠️ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘᴀss ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ ᴛᴏ ᴄʟᴏɴᴇ ᴛʜᴇɪʀ ᴘʟᴀʏʟɪsᴛ.\n\n📌 Example: `/cloneplaylist @username`"
        )

    if target_user_id == user_id:
        return await message.reply_text("ʜᴏᴡ ᴜsᴇʀ ᴄᴀɴ ᴄʟᴏɴᴇ ᴏᴡɴ ᴘʟᴀʏʟɪsᴛ ?")

    target_playlist = await _get_playlists(target_user_id)
    if not target_playlist:
        return await message.reply_text("ᴛʜᴇ ᴜsᴇʀ ʜᴀs ɴᴏᴛ ᴄʀᴇᴀᴛᴇᴅ ᴀɴʏ ᴘʟᴀʏʟɪsᴛ.")

    user_playlist = await _get_playlists(user_id)
    for name, data in target_playlist.items():
        if name not in user_playlist:
            await save_playlist(user_id, name, data)

            if "clone_count" not in data:
                data["clone_count"] = 0
            data["clone_count"] += 1
            await update_playlist(target_user_id, name, data)

    await message.reply_text(
        "ᴀʟʟ sᴏɴɢs ғʀᴏᴍ ᴛʜᴇ ᴜsᴇʀ'ꜱ ᴘʟᴀʏʟɪsᴛ ʜᴀᴠᴇ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ."
    )

    # Notify the original user
    try:
        cloner = message.from_user
        mention = f"<a href='tg://user?id={cloner.id}'>{cloner.first_name}</a>"

        target_user = await client.get_users(target_user_id)
        po_mention = (
            f"<a href='tg://user?id={target_user.id}'>{target_user.first_name}</a>"
        )

        notify_msg = (
            f"ʜᴇʏ {po_mention},\n\n" f"{mention} ᴊᴜsᴛ ᴄʟᴏɴᴇᴅ ʏᴏᴜʀ ᴘʟᴀʏʟɪsᴛ...🌸"
        )

        await client.send_message(
            target_user.id, notify_msg, disable_web_page_preview=True
        )

    except Exception as e:
        print(f"[CLONE NOTIFY ERROR] {e}")
