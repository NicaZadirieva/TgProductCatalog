from aiogram.types import InlineKeyboardButton, KeyboardButton

CREATE_KEYBOARD_TITLE = "Создать товар"
CREATE_PRODUCT_CB_DATA = "create_product"

create_product_inline_kb_btn = InlineKeyboardButton(
    text=CREATE_KEYBOARD_TITLE, callback_data=CREATE_PRODUCT_CB_DATA
)

create_product_menu_kb_btn = KeyboardButton(text=CREATE_KEYBOARD_TITLE)
