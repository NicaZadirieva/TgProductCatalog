import logging
from typing import BinaryIO

import httpx

from shared.errors.backend_api_error import BackendApiError
from shared.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()  # type: ignore


async def create_product(name: str, file: BinaryIO):
    data = {"original_photo": file, "name": name}
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            resp = await client.post(
                f"{settings.BACKEND_URL}/product/create", data=data
            )
    except httpx.HTTPError as e:
        logger.error("Не удалось связаться с API", exc_info=e)
        raise

    if resp.status_code != 201:
        logger.error(
            "Ошибка API: ",
            extra={"status_code": resp.status_code, "error": resp.text},
        )
        raise BackendApiError(message=resp.text, status_code=resp.status_code)
