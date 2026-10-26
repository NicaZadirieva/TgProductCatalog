import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.products.routes import router as product_router
from app.shared.settings import Settings
from app.utils.logs_util import LoggerUtils

logger = logging.getLogger(__name__)


def create_app():
    LoggerUtils.setup_logger()
    logger.debug("Запуск API")
    settings = Settings()  # type: ignore
    new_app = FastAPI(
        title="TgProductCatalog API",
        description="API для работы приложения Каталог товаров",
        version="0.0.1",
        openapi_tags=[
            {"name": "Products", "description": "Управление товарами"},
        ],
    )
    origins = [settings.common_app.FRONTEND_URL, settings.common_app.TELEGRAM_BOT_URL]
    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    new_app.state.settings = settings

    new_app.include_router(product_router)
    return new_app


app = create_app()
