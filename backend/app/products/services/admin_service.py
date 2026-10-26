from typing import Annotated

from fastapi import Depends

from app.shared.settings import Settings

settings = Settings()  # type: ignore


class AdminService:
    def __init__(self, admin_ids: list[int]):
        self.admin_ids = admin_ids

    def is_admin(self, user_id: int):
        return user_id in self.admin_ids


def get_admin_service():
    return AdminService(admin_ids=settings.common_app.TELEGRAM_ADMIN_IDS)


AdminServiceDeps = Annotated[AdminService, Depends(get_admin_service)]
