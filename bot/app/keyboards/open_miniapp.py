from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo

from app.shared.settings import Settings

settings = Settings()  # type: ignore
KEYBOARD_TITLE = "Открыть каталог"
open_miniapp_inline_kb_btn = InlineKeyboardButton(
    text=KEYBOARD_TITLE,
    callback_data="open_miniapp",
    web_app=WebAppInfo(url=settings.common_app.MINI_APP_URL),
)

open_miniapp_menu_kb_btn = KeyboardButton(
    text=KEYBOARD_TITLE, web_app=WebAppInfo(url=settings.common_app.MINI_APP_URL)
)
