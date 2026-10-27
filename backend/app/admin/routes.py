import logging

from fastapi import APIRouter

from app.middleware.is_admin import AdminUserIdDeps

router = APIRouter(prefix="/v1/admin", tags=["Admin"])

logger = logging.getLogger(__name__)


@router.get("/is", status_code=200)
def is_admin(telegram_id: AdminUserIdDeps):
    return True
