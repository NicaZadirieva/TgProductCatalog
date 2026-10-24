import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)


def create_app():
    logger.debug("Запуск API")
    app = FastAPI()  # TODO: настроить
    return app


app = create_app()
