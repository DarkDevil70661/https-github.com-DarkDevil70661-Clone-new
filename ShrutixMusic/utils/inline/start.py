from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
import config
from ShrutixMusic import nand


# ---------------- GROUP START PANEL ---------------- #

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{nand.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
                icon_custom_emoji_id=5445284980978621387
            ),
            InlineKeyboardButton(
                text=_["S_B_2"],
                style=ButtonStyle.SUCCESS,
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id=5395732581780040886
            ),
        ],
    ]
    return buttons


# ---------------- PRIVATE START PANEL ---------------- #

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                style=ButtonStyle.DANGER,
                url=f"https://t.me/{nand.username}?startgroup=true",
                icon_custom_emoji_id=5445284980978621387
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                style=ButtonStyle.PRIMARY,
                url="https://t.me/II_SCAM_01II",
                icon_custom_emoji_id=6084365261241061658   # ❗ Your emoji ID
            ),
            InlineKeyboardButton(
                text=_["S_B_12"],
                style=ButtonStyle.SUCCESS,
                callback_data="LG",
                icon_custom_emoji_id=4956560549287560231
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_2"],
                style=ButtonStyle.SUCCESS,
                url=config.SUPPORT_CHAT,
                icon_custom_emoji_id=5395732581780040886
            ),
            InlineKeyboardButton(
                text=_["S_B_6"],
                style=ButtonStyle.PRIMARY,
                url=config.SUPPORT_CHANNEL,
                icon_custom_emoji_id=5215668805199473901
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                style=ButtonStyle.DANGER,
                callback_data="settings_back_helper",
                icon_custom_emoji_id=5341715473882955310
            ),
        ],
    ]
    return buttons
