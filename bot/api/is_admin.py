import logging
from typing import BinaryIO

import httpx

from shared.errors.backend_api_error import BackendApiError
from shared.settings import Settings

logger = logging.getLogger(__name__)
settings = Settings()  # type: ignore


async def is_admin(telegram_id: int):
    try:
        async with httpx.AsyncClient(
            timeout=60.0, headers={"X-User-Id": str(telegram_id)}
        ) as client:
            resp = await client.get(
                f"{settings.BACKEND_URL}/admin/is",
            )
            if resp.status_code == 403:
                return False
            if resp.status_code != 200:
                logger.error(
                    "Ошибка API: ",
                    extra={
                        "status_code": resp.status_code,
                        "error": resp.text,
                        "telegram_id": telegram_id,
                    },
                )
                raise BackendApiError(message=resp.text, status_code=resp.status_code)
            return True
    except httpx.HTTPError as e:
        logger.error(
            "Не удалось связаться с API", exc_info=e, extra={"telegram_id": telegram_id}
        )
        raise
