from aiogram.types import InlineKeyboardButton, KeyboardButton

KEYBOARD_TITLE = "Открыть каталог"
open_miniapp_inline_kb_btn = InlineKeyboardButton(
    text=KEYBOARD_TITLE, callback_data="open_miniapp"
)

open_miniapp_menu_kb_btn = KeyboardButton(text=KEYBOARD_TITLE)
