from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ButtonStyle

from ShrutixMusic import nand


def help_pannel(_, START: Union[bool, int] = None):
    first = [
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"],
            callback_data="close",
            style=ButtonStyle.DANGER,
            icon_custom_emoji_id=5220108512893344933
        )
    ]

    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settings_back_helper",
            style=ButtonStyle.PRIMARY,
            icon_custom_emoji_id=6084861780935315826
        )
    ]

    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_25"],
                    callback_data="help_callback hb1",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5377754411319698237
                ),
                InlineKeyboardButton(
                    text=_["H_B_26"],
                    callback_data="help_callback hb2",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5251203410396458957
                ),
                InlineKeyboardButton(
                    text=_["H_B_28"],
                    callback_data="help_callback hb3",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5215668805199473901
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_27"],
                    callback_data="help_callback hb4",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5384234898494088007
                ),
                InlineKeyboardButton(
                    text=_["H_B_31"],
                    callback_data="help_callback hb6",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5938473438468378529
                ),
                InlineKeyboardButton(
                    text=_["H_B_29"],
                    callback_data="help_callback hb7",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5341806819247401359
                ),
            ],
            [
                InlineKeyboardButton(
                    text=_["H_B_33"],
                    callback_data="help_callback hb11",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5294339927318739359
                ),
                InlineKeyboardButton(
                    text=_["H_B_30"],
                    callback_data="help_callback hb9",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5197269100878907942
                ),
                InlineKeyboardButton(
                    text=_["H_B_32"],
                    callback_data="help_callback hb10",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=5373066076558996568
                ),
            ],
            mark,
        ]
    )

    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                    style=ButtonStyle.PRIMARY,
                    icon_custom_emoji_id=6084861780935315826
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{nand.username}?start=help",
            ),
        ],
    ]
    return buttons
