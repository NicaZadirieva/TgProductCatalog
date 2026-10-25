from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # TODO: добавить обращение к API. id из message.from_user.id
        return True


class IsAdminCallback(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return True  # callback.from_user.id
