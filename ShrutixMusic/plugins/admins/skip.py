from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from ShrutixMusic import YouTube, nand
from ShrutixMusic.core.call import Shruti
from ShrutixMusic.misc import db
from ShrutixMusic.utils.database import get_loop
from ShrutixMusic.utils.decorators import AdminRightsCheck
from ShrutixMusic.utils.inline import close_markup, stream_markup
from ShrutixMusic.utils.stream.autoclear import auto_clean
from ShrutixMusic.utils.thumbnails import get_thumb
from config import BANNED_USERS


@nand.on_message(
    filters.command(["skip", "cskip", "next", "cnext"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def skip(_, message: Message, __, chat_id):
    # ────────── SKIP WITH COUNT (/skip 2) ──────────
    if len(message.command) > 1:
        loop = await get_loop(chat_id)
        if loop != 0:
            return await message.reply_text(__["admin_8"])

        state = message.command[1]
        if not state.isnumeric():
            return await message.reply_text(__["admin_9"])

        state = int(state)
        check = db.get(chat_id)
        if not check:
            return await message.reply_text(__["queue_2"])

        count = len(check) - 1
        if count < 1:
            return await message.reply_text(__["admin_10"])

        if not 1 <= state <= count:
            return await message.reply_text(__["admin_11"].format(count))

        for _ in range(state):
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)

        if not check:
            await message.reply_text(
                __["admin_6"].format(
                    message.from_user.mention,
                    message.chat.title,
                ),
                reply_markup=close_markup(__),
            )
            return await Shruti.stop_stream(chat_id)

    # ────────── NORMAL SKIP (/skip) ──────────
    else:
        check = db.get(chat_id)
        if not check:
            return await message.reply_text(__["queue_2"])

        popped = check.pop(0)
        if popped:
            await auto_clean(popped)

        if not check:
            await message.reply_text(
                __["admin_6"].format(
                    message.from_user.mention,
                    message.chat.title,
                ),
                reply_markup=close_markup(__),
            )
            return await Shruti.stop_stream(chat_id)

    # ────────── PLAY NEXT TRACK ──────────
    data = check[0]
    queued = data["file"]
    title = data["title"].title()
    user = data["by"]
    streamtype = data["streamtype"]
    videoid = data["vidid"]
    status = True if streamtype == "video" else None

    db[chat_id][0]["played"] = 0

    if data.get("old_dur"):
        db[chat_id][0]["dur"] = data["old_dur"]
        db[chat_id][0]["seconds"] = data["old_second"]
        db[chat_id][0]["speed_path"] = None
        db[chat_id][0]["speed"] = 1.0

    # ────────── HANDLE PLAYLIST TYPES ──────────

    # ▶ LIVE STREAM
    if "live_" in queued:
        n, link = await YouTube.video(videoid, True)
        if n == 0:
            return await message.reply_text(__["admin_7"].format(title))

        image = await YouTube.thumbnail(videoid, True)
        await Shruti.skip_stream(chat_id, link, video=status, image=image)

    # ▶ YOUTUBE VIDEO (PLAYLIST)
    elif "vid_" in queued:
        mystic = await message.reply_text(__["call_7"])
        file_path, _ = await YouTube.download(
            videoid,
            mystic,
            videoid=True,
            video=status,
        )
        image = await YouTube.thumbnail(videoid, True)
        await Shruti.skip_stream(chat_id, file_path, video=status, image=image)
        await mystic.delete()

    # ▶ TELEGRAM INDEX
    elif "index_" in queued:
        await Shruti.skip_stream(chat_id, videoid, video=status)

    # ▶ NORMAL FILE / AUDIO
    else:
        image = None
        if videoid not in ["telegram", "soundcloud"]:
            image = await YouTube.thumbnail(videoid, True)

        await Shruti.skip_stream(chat_id, queued, video=status, image=image)

    # ────────── NOW PLAYING MESSAGE ──────────
    button = stream_markup(__, chat_id)
    img = await get_thumb(videoid)

    run = await message.reply_photo(
        photo=img if img else config.STREAM_IMG_URL,
        caption=__["stream_1"].format(
            f"https://t.me/{nand.username}?start=info_{videoid}",
            title[:23],
            data["dur"],
            user,
        ),
        reply_markup=InlineKeyboardMarkup(button),
    )

    db[chat_id][0]["mystic"] = run
    db[chat_id][0]["markup"] = "stream"
