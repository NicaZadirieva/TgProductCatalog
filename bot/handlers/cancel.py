from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states.create_product import CreateProduct

cancel_router = Router()


@cancel_router.message(Command("cancel"), CreateProduct.waiting_for_data)
async def cancel_create_product(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Создание товара отменено.")
