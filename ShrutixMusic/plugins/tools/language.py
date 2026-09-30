from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message
from pyrogram.enums import ButtonStyle

from ShrutixMusic import nand
from ShrutixMusic.utils.database import get_lang, set_lang
from ShrutixMusic.utils.decorators import ActualAdminCB, language, languageCB
from config import BANNED_USERS
from strings import get_string


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)

    keyboard.add(
        InlineKeyboardButton(
            text="English ",
            callback_data="languages:en",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=5927292517610426176
        ),
        InlineKeyboardButton(
            text="தமிழ் ",
            callback_data="languages:ta",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=6082662276643425446
        ),
        InlineKeyboardButton(
            text="हिंदी",
            callback_data="languages:hi",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=6082662276643425446
        ),
        InlineKeyboardButton(
            text="عربي",
            callback_data="languages:es",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=5449495646656537594
        ),
    )

    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settingsback_helper",
            style=ButtonStyle.SUCCESS,
            icon_custom_emoji_id=6084861780935315826
        ),
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"],
            callback_data="close",
            style=ButtonStyle.DANGER,
            icon_custom_emoji_id=5220108512893344933
        ),
    )

    return keyboard


@nand.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"],
        reply_markup=keyboard,
    )


@nand.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@nand.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
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
