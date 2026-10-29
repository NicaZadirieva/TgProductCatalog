from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.filters.is_admin import IsAdmin
from app.keyboards import (
    create_admin_menu_keyboard,
    create_user_menu_keyboard,
)

start_router = Router()


@start_router.message(CommandStart(), IsAdmin())
async def cmd_admin_start(message: Message):
    await message.answer("У меня есть товар", reply_markup=create_admin_menu_keyboard())


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("У меня есть товар", reply_markup=create_user_menu_keyboard())
