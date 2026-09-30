import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ShrutixMusic import YouTube, nand
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import SUDOERS, db
from ShrutixMusic.utils.database import (
    get_active_chats,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_music_playing,
    is_nonadmin_chat,
    music_off,
    music_on,
    set_loop,
)
from ShrutixMusic.utils.decorators.language import languageCB
from ShrutixMusic.utils.formatters import seconds_to_min
from ShrutixMusic.utils.inline import close_markup, stream_markup, stream_markup_timer
from ShrutixMusic.utils.stream.autoclear import auto_clean
from ShrutixMusic.utils.thumbnails import get_thumb
from config import (
    BANNED_USERS,
    SUPPORT_CHAT,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    confirmer,
    votemode,
)
from strings import get_string

checker = {}
upvoters = {}

# ---------------- CLOSE BUTTON CALLBACK ---------------- #

@nand.on_callback_query(filters.regex("^close$") & ~BANNED_USERS)
async def close_callback(client, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass

    try:
        await CallbackQuery.message.delete()
    except:
        try:
            await CallbackQuery.edit_message_reply_markup(reply_markup=None)
        except:
            pass


# ---------------- ADMIN CALLBACK ---------------- #

@nand.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")

    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]

    chat_id = int(chat)

    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)

    mention = CallbackQuery.from_user.mention

    # ---------- UPVOTE ----------
    if command == "UpVote":
        if chat_id not in votemode:
            votemode[chat_id] = {}
        if chat_id not in upvoters:
            upvoters[chat_id] = {}

        if CallbackQuery.message.id not in upvoters[chat_id]:
            upvoters[chat_id][CallbackQuery.message.id] = []

        if CallbackQuery.message.id not in votemode[chat_id]:
            votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            upvoters[chat_id][CallbackQuery.message.id].remove(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            upvoters[chat_id][CallbackQuery.message.id].append(
                CallbackQuery.from_user.id
            )
            votemode[chat_id][CallbackQuery.message.id] += 1

        upvote = await get_upvote_count(chat_id)
        current_votes = votemode[chat_id][CallbackQuery.message.id]

        if current_votes >= upvote:
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]

                if (
                    current["vidid"] != exists["vidid"]
                    or current["file"] != exists["file"]
                ):
                    return await CallbackQuery.edit_message_text(_["admin_35"])

                await CallbackQuery.edit_message_text(
                    _["admin_37"].format(upvote)
                )
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])

            command = counter
            mention = "ᴜᴘᴠᴏᴛᴇs"
        else:
            upl = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        text=f"👍 {current_votes}",
                        callback_data=f"ADMIN  UpVote|{chat_id}_{counter}",
                    )
                ]]
            )
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)

    # ---------- ADMIN CHECK ----------
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin and CallbackQuery.from_user.id not in SUDOERS:
            admins = adminlist.get(CallbackQuery.message.chat.id, [])
            if CallbackQuery.from_user.id not in admins:
                return await CallbackQuery.answer(
                    _["admin_14"], show_alert=True
                )

    # ---------- CONTROLS ----------
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await music_off(chat_id)
        await Shruti.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            _["admin_2"].format(mention),
            reply_markup=close_markup(_),
        )

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await music_on(chat_id)
        await Shruti.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            _["admin_4"].format(mention),
            reply_markup=close_markup(_),
        )

    elif command in ["Stop", "End"]:
        await Shruti.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(
            _["admin_5"].format(mention),
            reply_markup=close_markup(_),
        )
        await CallbackQuery.message.delete()

    elif command in ["Skip", "Replay"]:
        check = db.get(chat_id)
        txt = (
            f"➻ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ 🎄\n│\n└ʙʏ : {mention} 🥀"
            if command == "Skip"
            else f"➻ sᴛʀᴇᴀᴍ ʀᴇ-ᴘʟᴀʏᴇᴅ 🎄\n│\n└ʙʏ : {mention} 🥀"
        )

        try:
            popped = check.pop(0)
            await auto_clean(popped)
        except:
            pass

        if not check:
            await Shruti.stop_stream(chat_id)
            return

        await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))


# ---------------- STREAM TIMER ---------------- #

async def markup_timer():
    while not await asyncio.sleep(7):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            if not await is_music_playing(chat_id):
                continue

            playing = db.get(chat_id)
            if not playing:
                continue

            try:
                mystic = playing[0]["mystic"]
                language = await get_lang(chat_id)
                _ = get_string(language)
                buttons = stream_markup_timer(
                    _,
                    chat_id,
                    seconds_to_min(playing[0]["played"]),
                    playing[0]["dur"],
                )
                await mystic.edit_reply_markup(
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
            except:
                continue


asyncio.create_task(markup_timer())
