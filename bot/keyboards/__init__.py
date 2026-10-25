from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from .create_product import create_product_inline_kb_btn, create_product_menu_kb_btn
from .open_miniapp import open_miniapp_inline_kb_btn, open_miniapp_menu_kb_btn


def create_admin_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[create_product_inline_kb_btn, open_miniapp_inline_kb_btn]]
    )


def create_admin_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [create_product_menu_kb_btn, open_miniapp_menu_kb_btn],
        ],
        resize_keyboard=True,
    )


def create_user_inline_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[open_miniapp_inline_kb_btn]])


def create_user_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [open_miniapp_menu_kb_btn],
        ],
        resize_keyboard=True,
    )
