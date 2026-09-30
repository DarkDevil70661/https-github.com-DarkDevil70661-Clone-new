import time
import asyncio

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from py_yt import VideosSearch

import config
from ShrutixMusic import nand
from ShrutixMusic.misc import _boot_
from ShrutixMusic.plugins.sudo.sudoers import sudoers_list
from ShrutixMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from ShrutixMusic.utils.decorators.language import LanguageStart
from ShrutixMusic.utils.formatters import get_readable_time
from ShrutixMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


# ───────────── PRIVATE START ───────────── #

@nand.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)

    # ───── START WITH ARG ───── #
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]

        # HELP
        if name.startswith("help"):
            return await nand.send_photo(
                chat_id=message.chat.id,
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=help_pannel(_),
                has_spoiler=True,
            )

        # SUDO LIST
        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await nand.send_message(
                    config.LOGGER_ID,
                    f"{message.from_user.mention} checked <b>sudo list</b>\n\n"
                    f"ID: <code>{message.from_user.id}</code>",
                )
            return

        # TRACK INFO
        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            video_id = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={video_id}"

            results = VideosSearch(query, limit=1)
            data = await results.next()

            if not data.get("result"):
                return await m.edit_text("❌ Video not found.")

            r = data["result"][0]

            title = r.get("title", "Unknown")
            duration = r.get("duration", "Unknown")
            views = r.get("viewCount", {}).get("short", "N/A")
            published = r.get("publishedTime", "N/A")
            thumbnail = r.get("thumbnails", [{}])[0].get("url")
            link = r.get("link", config.SUPPORT_CHAT)

            channel = r.get("channel", {})
            channel_name = channel.get("name", "Unknown")

            channellink = (
                channel.get("link")
                or (f"https://t.me/{channel['username']}" if channel.get("username") else None)
                or link
            )

            text = _["start_6"].format(
                title,
                duration,
                views,
                published,
                channellink,
                channel_name,
                nand.mention,
            )

            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(_["S_B_8"], url=link),
                        InlineKeyboardButton(_["S_B_9"], url=config.SUPPORT_CHAT),
                    ]
                ]
            )

            await m.delete()
            await nand.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=text,
                reply_markup=buttons,
            )

            if await is_on_off(2):
                await nand.send_message(
                    config.LOGGER_ID,
                    f"{message.from_user.mention} checked track info\n"
                    f"ID: <code>{message.from_user.id}</code>",
                )
            return

    # ───── NORMAL START ───── #
    await nand.send_photo(
    chat_id=message.chat.id,
    photo=config.START_IMG_URL,
    caption=_["start_2"].format(message.from_user.mention, nand.mention),
    reply_markup=InlineKeyboardMarkup(private_panel(_)),
    has_spoiler=True,
)


# ───────────── GROUP START ───────────── #

@nand.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(
            nand.mention,
            get_readable_time(uptime),
        ),
        reply_markup=InlineKeyboardMarkup(start_panel(_)),
    )
    await add_served_chat(message.chat.id)


# ───────────── WELCOME ───────────── #

@nand.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            _ = get_string(await get_lang(message.chat.id))

            if await is_banned_user(member.id):
                return await message.chat.ban_member(member.id)

            if member.id != nand.id:
                return

            if message.chat.type != ChatType.SUPERGROUP:
                await message.reply_text(_["start_4"])
                return await nand.leave_chat(message.chat.id)

            if message.chat.id in await blacklisted_chats():
                await message.reply_text(
                    _["start_5"].format(
                        nand.mention,
                        f"https://t.me/{nand.username}?start=sudolist",
                        config.SUPPORT_CHAT,
                    ),
                    disable_web_page_preview=True,
                )
                return await nand.leave_chat(message.chat.id)

            await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["start_3"].format(
                    message.from_user.first_name,
                    nand.mention,
                    message.chat.title,
                    nand.mention,
                ),
                reply_markup=InlineKeyboardMarkup(start_panel(_)),
            )

            await add_served_chat(message.chat.id)
            await message.stop_propagation()

        except Exception as e:
            print("WELCOME ERROR:", e)
