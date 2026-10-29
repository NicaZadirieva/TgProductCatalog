import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.cancel import cancel_router
from handlers.create_product import product_router
from handlers.start import start_router
from shared.settings import Settings
from utils.logs_util import LoggerUtils


async def main():
    LoggerUtils.setup_logger()
    settings = Settings()  # type: ignore

    bot = Bot(token=settings.tg_app.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(cancel_router)
    dp.include_router(product_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
