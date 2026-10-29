import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from shared.settings import Settings

settings = Settings()  # type: ignore
logger = logging.getLogger(__name__)

bot = Bot(token=settings.tg_app.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
