import asyncio

from create_bot import bot, dp
from handlers.cancel import cancel_router
from handlers.create_product import product_router
from handlers.start import start_router


async def main():
    dp.include_router(start_router)
    dp.include_router(cancel_router)
    dp.include_router(product_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
