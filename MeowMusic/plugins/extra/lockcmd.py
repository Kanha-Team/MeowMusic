# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from MeowMusic import app
from MeowMusic.utils.database import (
    add_locked_command,
    get_locked_commands,
    remove_locked_command,
)

LOCKABLE_CMDS = [
    "id",
    "info",
    "afk",
    "git",
    "left",
    "couples",
    "report",
    "packkang",
    "addsong",
    "playlist",
    "delplaylist",
    "playplaylist",
    "cloneplaylist",
]

# Define locktypes and descriptions
LOCKABLE_CMDS_INFO = {
    "id": "Shows the ID of the user, chat, or replied message.",
    "info": "Gives detailed user info like username, ID, bio, etc.",
    "afk": "Sets your status as AFK (Away From Keyboard).",
    "git": "Displays the info of given github link.",
    "left": "Used to track or log users who leave the group.",
    "couples": "Shows random couple pairings in the group.",
    "report": "Reports a message or user to admins for moderation.",
    "packkang": "Steals sticker packs (used to save/download them).",
    "addsong": "Adds a song to playlist.",
    "playlist": "Displays saved playlist (music commands).",
    "delplaylist": "Deletes a song from saved playlist.",
    "playplaylist": "Plays songs from playlist in voice chat.",
    "cloneplaylist": "Clones someone else's playlist into yours.",
}


def is_admin(member):
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


@app.on_message(filters.command("lock"))
async def lock_command_handler(client: Client, message: Message):
    args = message.text.split()

    if len(args) != 2:
        return await message.reply("Usage: `/lock [cmd name]`")

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Only for groups!")

    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if not is_admin(member):
            return await message.reply("You're not admin...")
    except:
        return

    cmd = message.command[1].lower().strip("/")
    if cmd not in LOCKABLE_CMDS:
        return await message.reply(f"'{cmd}' is not lockable...")

    await add_locked_command(message.chat.id, cmd)
    await message.reply(f"`{cmd}` command locked in this group...")


@app.on_message(filters.command("unlock"))
async def unlock_command_handler(client: Client, message: Message):
    args = message.text.split()

    if len(args) != 2:
        return await message.reply("Usage: `/unlock [cmd name]`")

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("Only for groups!")

    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        if not is_admin(member):
            return await message.reply("You're not admin...")
    except:
        return

    cmd = message.command[1].lower().strip("/")
    if cmd not in LOCKABLE_CMDS:
        return await message.reply(f"'{cmd}' is not lockable...")

    locked_cmds = await get_locked_commands(message.chat.id)
    if cmd not in locked_cmds:
        return await message.reply(f"`{cmd}` is not locked in this group..!")

    await remove_locked_command(message.chat.id, cmd)
    await message.reply(f"`{cmd}` command unlocked successfully!")


@app.on_message(filters.command("locked"))
async def show_locked_cmds(client: Client, message: Message):
    locked = await get_locked_commands(message.chat.id)
    if not locked:
        return await message.reply("No commands are locked..")

    await message.reply(
        "🔒 Locked commands:\n" + "\n".join(f"• `{cmd}`" for cmd in locked)
    )


@app.on_message(filters.command("locktypes"))
async def show_locktypes(client, message: Message):
    buttons = []
    row = []
    for i, lock in enumerate(LOCKABLE_CMDS_INFO):
        row.append(InlineKeyboardButton(lock, callback_data=f"locktype_{lock}"))
        if (i + 1) % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    # ✅ Extra action buttons
    buttons.append(
        [
            InlineKeyboardButton("📋 Lock List", callback_data="copy_format"),
            InlineKeyboardButton("❓ How to Use", callback_data="help_lock"),
        ]
    )

    # ❌ Close button
    buttons.append([InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")])

    await message.reply(
        "🔒 The available cmd locktypes are:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(r"locktype_(.*)"))
async def locktype_info(client, callback_query: CallbackQuery):
    lock = callback_query.data.split("_", 1)[1]
    desc = LOCKABLE_CMDS_INFO.get(lock, "No info available.")
    await callback_query.answer(f"/{lock}:\n\n{desc}", show_alert=True)


@app.on_callback_query(filters.regex("copy_format"))
async def send_copy_format(client, callback_query: CallbackQuery):
    cmds = "\n".join(f"• `{cmd}`" for cmd in LOCKABLE_CMDS_INFO)
    await callback_query.message.edit_text(
        f"📋 **Copyable Lock Commands:**\n\n{cmds}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_locktypes")]]
        ),
    )


@app.on_callback_query(filters.regex("help_lock"))
async def send_lock_help(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "**🔐 How to use Lock System:**\n\n"
        "`/lock [command]` – Lock a specific command.\n"
        "`/unlock [command]` – Unlock a previously locked command.\n"
        "`/locked` – Show currently locked commands in the group.\n\n"
        "**📝 Example Usage:**\n"
        "`/lock id` → Blocks usage of /id in group\n"
        "`/unlock id` → Allows /id again\n\n"
        "**🔒 Note:**\n"
        "• Works only in groups\n"
        "• Only admins can lock/unlock\n"
        "• Use `/locktypes` to see which commands can be locked\n",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="back_locktypes")]]
        ),
    )


@app.on_callback_query(filters.regex("back_locktypes"))
async def go_back_to_locktypes(client, callback_query: CallbackQuery):
    # re-generate the buttons same as show_locktypes
    buttons = []
    row = []
    for i, lock in enumerate(LOCKABLE_CMDS_INFO):
        row.append(InlineKeyboardButton(lock, callback_data=f"locktype_{lock}"))
        if (i + 1) % 3 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton("📋 Lock List", callback_data="copy_format"),
            InlineKeyboardButton("❓ How to Use", callback_data="help_lock"),
        ]
    )
    buttons.append([InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")])

    await callback_query.message.edit_text(
        "🔒 The available cmd locktypes are:",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
