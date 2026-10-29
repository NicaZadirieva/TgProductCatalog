import logging

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.create_bot import bot, dp
from app.handlers.cancel import cancel_router
from app.handlers.create_product import product_router
from app.handlers.start import start_router
from app.shared.settings import Settings

settings = Settings()  # type: ignore

WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{settings.webhook.WEBHOOK_HOST}{WEBHOOK_PATH}"


async def on_startup(bot) -> None:
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(bot) -> None:
    await bot.delete_webhook()


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    dp.include_router(start_router)
    dp.include_router(cancel_router)
    dp.include_router(product_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()

    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(
        app, host=settings.webhook.WEBAPP_HOST, port=settings.webhook.WEBAPP_PORT
    )


if __name__ == "__main__":
    main()
