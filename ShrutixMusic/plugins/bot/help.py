from typing import Union

from pyrogram import filters, types
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.utils import help_pannel
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.decorators.language import LanguageStart, languageCB
from ShrutixMusic.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers


# ================= PRIVATE HELP ================= #
@nand.on_message(filters.command("help") & filters.private & ~BANNED_USERS)
@nand.on_callback_query(filters.regex("^settings_back_helper$") & ~BANNED_USERS)
async def helper_private(
    client: nand,
    update: Union[types.Message, types.CallbackQuery],
):
    # ---------- CALLBACK ----------
    if isinstance(update, types.CallbackQuery):
        try:
            await update.answer()
        except:
            pass

        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)

        keyboard = help_pannel(_)

        try:
            await update.edit_message_text(
                _["help_1"].format(SUPPORT_CHAT),
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
        except MessageNotModified:
            pass

    # ---------- PRIVATE MESSAGE ----------
    else:
        try:
            await update.delete()
        except:
            pass

        language = await get_lang(update.chat.id)
        _ = get_string(language)

        keyboard = help_pannel(_)

        # ❌ NO disable_web_page_preview HERE (PHOTO)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


# ================= GROUP HELP ================= #
@nand.on_message(filters.command("help") & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)

    await message.reply_text(
        _["help_2"].format(SUPPORT_CHAT),
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
    )


# ================= HELP CALLBACK ================= #
@nand.on_callback_query(filters.regex("^help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    keyboard = help_back_markup(_)

    HELP_MAP = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
    }

    text = HELP_MAP.get(cb)
    if not text:
        return

    try:
        await CallbackQuery.edit_message_text(
            text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )
    except MessageNotModified:
        pass
