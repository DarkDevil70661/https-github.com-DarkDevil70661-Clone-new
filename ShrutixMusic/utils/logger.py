from pyrogram.enums import ParseMode

from ShrutixMusic import nand
from ShrutixMusic.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    # Check logger toggle
    if not await is_on_off(2):
        return

    # ---------- SAFE QUERY EXTRACTION ----------
    query = "No query provided"
    if message.text:
        parts = message.text.split(None, 1)
        if len(parts) > 1:
            query = parts[1]

    # ---------- SAFE CHAT DETAILS ----------
    chat_title = message.chat.title or "Private Chat"
    chat_username = f"@{message.chat.username}" if message.chat.username else "None"

    # ---------- SAFE USER DETAILS ----------
    user_username = (
        f"@{message.from_user.username}"
        if message.from_user and message.from_user.username
        else "None"
    )

    user_mention = (
        message.from_user.mention
        if message.from_user
        else "Anonymous"
    )

    user_id = message.from_user.id if message.from_user else "Unknown"

    # ---------- LOGGER MESSAGE ----------
    logger_text = f"""
<b>{nand.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> {chat_title}
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> {chat_username}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{user_id}</code>
<b>ɴᴀᴍᴇ :</b> {user_mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> {user_username}

<b>ǫᴜᴇʀʏ :</b> {query}
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> {streamtype}
"""

    # ---------- SEND LOG ----------
    if message.chat.id != LOGGER_ID:
        try:
            await nand.send_message(
                chat_id=LOGGER_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception:
            pass
