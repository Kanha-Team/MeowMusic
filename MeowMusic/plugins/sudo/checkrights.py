# Copyright (C) 2026 by Kanha-Team@Github, < https://github.com/Kanha-Team>.
#
# This file is part of < https://github.com/Kanha-Team/MeowMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Kanha-Team/MeowMusic/blob/main/LICENSE >
#
# All rights reserved


from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from config import OWNER_ID
from MeowMusic import app


@app.on_message(filters.command("checkrights") & filters.user(OWNER_ID))
async def check_rights(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("⚠️ Please provide a group chat ID.")
        return

    chat_id = message.command[1]

    try:
        member = await client.get_chat_member(chat_id, client.me.id)

        if member.status == ChatMemberStatus.ADMINISTRATOR:
            privileges = member.privileges
            admin_rights = f"""
🔹 Bot Admin Rights in {chat_id}
👑 Is Admin: ✅ Yes
📌 Can Change Info: {'✅' if privileges.can_change_info else '❌'}
🚷 Can Restrict Members: {'✅' if privileges.can_restrict_members else '❌'}
🚮 Can Delete Messages: {'✅' if privileges.can_delete_messages else '❌'}
🚪 Can Invite Users: {'✅' if privileges.can_invite_users else '❌'}
🔇 Can Manage Voice Chats: {'✅' if privileges.can_manage_video_chats else '❌'}
📢 Can Post Messages: {'✅' if privileges.can_post_messages else '❌'}
🔧 Can Manage Chat: {'✅' if privileges.can_manage_chat else '❌'}
⚠️ Can Add Admins: {'✅' if privileges.can_promote_members else '❌'}
            """
            await message.reply_text(admin_rights)
        else:
            await message.reply_text("❌ Bot is not an admin in this chat.")

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e!s}")
