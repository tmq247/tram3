from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import ChatAdminRequired
from config import LOGGER_ID as LOG_GROUP_ID
from Radha import app  


@app.on_message(filters.new_chat_members, group=2)
async def join_watcher(_, message):    
    chat = message.chat
    link = "❌ Bot lacks permission to fetch invite link."
    
    try:
        # Try to fetch the invite link
        member = await app.get_chat_member(chat.id, "me")
        if member.status in ("administrator", "creator"):
            link = await app.export_chat_invite_link(chat.id)
    except ChatAdminRequired:
        pass  # Bot isn't admin or lacks permission

    for member in message.new_chat_members:
        if member.id == app.id:
            count = await app.get_chat_members_count(chat.id)

            msg = (
                f"🎵 Music bot added to a new group!\n\n"
                f"➤ Chat Name: {chat.title}\n"
                f"➤ Chat ID: <code>{chat.id}</code>\n"
                f"➤ Username: @{chat.username if chat.username else 'No username'}\n"
                f"➤ Invite Link: {link}\n"
                f"➤ Members Count: {count}\n"
                f"➤ Added By: {message.from_user.mention}"
            )
            await app.send_message(LOG_GROUP_ID, msg)


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    if (await app.get_me()).id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "Unknown"
        title = message.chat.title
        username = f"@{message.chat.username}" if message.chat.username else "Private chat"
        chat_id = message.chat.id

        left_msg = (
            f"🚫 Bot removed from a group!\n\n"
            f"➤ Chat Title: {title}\n"
            f"➤ Chat ID: <code>{chat_id}</code>\n"
            f"➤ Removed By: {removed_by}\n"
            f"➤ Group Username: {username}"
        )
        await app.send_message(LOG_GROUP_ID, left_msg)