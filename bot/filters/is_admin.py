from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message

from api.is_admin import is_admin


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            return await is_admin(message.from_user.id)  # type: ignore
        except:  # noqa: E722
            return False


class IsAdminCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        try:
            return await is_admin(callback.from_user.id)
        except:  # noqa: E722
            return False
