import logging
import os

import httpx
from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from api.create_product import create_product
from filters.is_admin import IsAdmin, IsAdminCallback
from keyboards.create_product import CREATE_KEYBOARD_TITLE, CREATE_PRODUCT_CB_DATA
from shared.errors.backend_api_error import BackendApiError
from states.create_product import CreateProduct

logger = logging.getLogger(__name__)

product_router = Router()
product_router.message.filter(IsAdmin())
product_router.callback_query.filter(IsAdminCallback())

PROMPT = "Введите название товара и приложите фото одним сообщением"


@product_router.callback_query(F.data == CREATE_PRODUCT_CB_DATA)
async def handle_create_product_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    if not isinstance(callback.message, Message):
        # сообщение удалено или слишком старое
        return
    await state.set_state(CreateProduct.waiting_for_data)
    await callback.message.answer(PROMPT)


@product_router.message(F.text == CREATE_KEYBOARD_TITLE)
async def handle_create_product(message: Message, state: FSMContext):
    await state.set_state(CreateProduct.waiting_for_data)
    await message.answer(PROMPT)


@product_router.message(CreateProduct.waiting_for_data, F.photo)
async def process_product_data(message: Message, state: FSMContext, bot: Bot):
    title = message.caption
    if not title:
        await message.answer("Пожалуйста, отправьте фото с названием товара в подписи.")
        return
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото")
        return

    photo_file = message.photo[-1]
    file = await bot.get_file(photo_file.file_id)
    if not file.file_path:
        await message.answer("Сервер не передал всю информацию о фото. Повторите позже")
        return
    _, file_extension = os.path.splitext(file.file_path)
    file_obj = await bot.download_file(file.file_path)
    if not file_obj:
        await message.answer("Сервер не передал всю информацию о фото. Повторите позже")
        return
    try:
        await create_product(
            telegram_id=message.from_user.id,
            name=title,
            file=file_obj,
            file_extension=file_extension,
        )

        await state.clear()
        await message.answer("Товар сохранен успешно")
    except httpx.HTTPError as e:
        await message.answer(
            "Не удалось связаться с API. Повторите позже. \\cancel - отменить"
        )
    except BackendApiError as e:
        await message.answer("Ошибка API. Повторите позже. \\cancel - отменить")


@product_router.message(CreateProduct.waiting_for_data)
async def process_product_wrong_input(message: Message, state: FSMContext):
    await message.answer(
        "Нужно именно фото с названием товара в подписи. Попробуйте еще раз "
        "или введите /cancel для отмены."
    )
