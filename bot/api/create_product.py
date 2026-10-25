import logging
import mimetypes
from typing import BinaryIO

import httpx

from shared.errors.backend_api_error import BackendApiError
from shared.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()  # type: ignore


async def create_product(
    telegram_id: int, name: str, file: BinaryIO, file_extension: str
):
    data = {"name": name}
    filename = f"original_photo{file_extension}"
    content_type = mimetypes.guess_type(filename)[0] or "image/jpeg"

    try:
        async with httpx.AsyncClient(
            timeout=60.0, headers={"X-User-Id": str(telegram_id)}
        ) as client:
            file.seek(0)
            resp = await client.post(
                f"{settings.BACKEND_URL}/product/create",
                data=data,
                files={"original_photo": (filename, file, content_type)},
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
