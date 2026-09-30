from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ShrutixMusic import nand
from ShrutixMusic.misc import SUDOERS, db
from ShrutixMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
)
from config import SUPPORT_CHAT, adminlist, confirmer
from strings import get_string

from ..formatters import int_to_alpha


# ==========================
# ADMIN RIGHTS CHECK (MAIN)
# ==========================
def AdminRightsCheck(mystic):
    async def wrapper(client, message, *args, **kwargs):

        # Maintenance check
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    f"{nand.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, "
                    f"ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        # Language
        try:
            lang = await get_lang(message.chat.id)
            _ = get_string(lang)
        except:
            _ = get_string("en")

        # Anonymous admin
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
            )
            return await message.reply_text(_["general_3"], reply_markup=upl)

        # Channel mode
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_7"])
            try:
                await nand.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
        else:
            chat_id = message.chat.id

        # Active VC check
        if not await is_active_chat(chat_id):
            return await message.reply_text(_["general_5"])

        # Admin permission
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin and message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_13"])

            if message.from_user.id not in admins:
                if await is_skipmode(message.chat.id):
                    upvote = await get_upvote_count(chat_id)

                    text = (
                        "<b>ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɴᴇᴇᴅᴇᴅ</b>\n\n"
                        "ʀᴇғʀᴇsʜ ᴀᴅᴍɪɴ ᴄᴀᴄʜᴇ ᴠɪᴀ : /reload\n\n"
                        f"» {upvote} ᴠᴏᴛᴇs ɴᴇᴇᴅᴇᴅ ғᴏʀ ᴘᴇʀғᴏʀᴍɪɴɢ ᴛʜɪs ᴀᴄᴛɪᴏɴ."
                    )

                    command = message.command[0].lstrip("c").lower()
                    if command == "speed":
                        return await message.reply_text(_["admin_14"])

                    MODE = command.title()
                    upl = InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ᴠᴏᴛᴇ", callback_data=f"ADMIN UpVote|{chat_id}_{MODE}")]]
                    )

                    if chat_id not in confirmer:
                        confirmer[chat_id] = {}

                    try:
                        vidid = db[chat_id][0]["vidid"]
                        file = db[chat_id][0]["file"]
                    except:
                        return await message.reply_text(_["admin_14"])

                    sent = await message.reply_text(text, reply_markup=upl)
                    confirmer[chat_id][sent.id] = {"vidid": vidid, "file": file}
                    return

                return await message.reply_text(_["admin_14"])

        # PASS EVERYTHING SAFELY
        return await mystic(client, message, _, chat_id, *args, **kwargs)

    return wrapper


# ==========================
# STRICT ADMIN CHECK
# ==========================
def AdminActual(mystic):
    async def wrapper(client, message, *args, **kwargs):

        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    f"{nand.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, "
                    f"ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a>",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            lang = await get_lang(message.chat.id)
            _ = get_string(lang)
        except:
            _ = get_string("en")

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [[InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ғɪx ?", callback_data="AnonymousAdmin")]]
            )
            return await message.reply_text(_["general_3"], reply_markup=upl)

        if message.from_user.id not in SUDOERS:
            try:
                member = (
                    await nand.get_chat_member(message.chat.id, message.from_user.id)
                ).privileges
            except:
                return
            if not member.can_manage_video_chats:
                return await message.reply_text(_["general_4"])

        return await mystic(client, message, _, *args, **kwargs)

    return wrapper


# ==========================
# CALLBACK ADMIN CHECK
# ==========================
def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery, *args, **kwargs):

        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{nand.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ",
                    show_alert=True,
                )

        try:
            lang = await get_lang(CallbackQuery.message.chat.id)
            _ = get_string(lang)
        except:
            _ = get_string("en")

        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery, _, *args, **kwargs)

        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                priv = (
                    await nand.get_chat_member(
                        CallbackQuery.message.chat.id,
                        CallbackQuery.from_user.id,
                    )
                ).privileges
            except:
                return await CallbackQuery.answer(_["general_4"], show_alert=True)

            if not priv.can_manage_video_chats:
                if CallbackQuery.from_user.id not in SUDOERS:
                    token = await int_to_alpha(CallbackQuery.from_user.id)
                    auth = await get_authuser_names(CallbackQuery.from_user.id)
                    if token not in auth:
                        return await CallbackQuery.answer(_["general_4"], show_alert=True)

        return await mystic(client, CallbackQuery, _, *args, **kwargs)

    return wrapper
