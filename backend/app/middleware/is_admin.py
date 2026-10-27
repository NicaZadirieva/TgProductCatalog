from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.admin.admin_service import AdminServiceDeps


def get_current_user_id(
    x_user_id: Annotated[
        int, Header(alias="X-User-Id")
    ],  # TODO: подумать как сделать безопаснее
) -> int:
    return x_user_id


CurrentUserIdDeps = Annotated[int, Depends(get_current_user_id)]


def require_admin(
    user_id: CurrentUserIdDeps,
    admin_service: AdminServiceDeps,
) -> int:
    if not admin_service.is_admin(user_id):
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )
    return user_id


AdminUserIdDeps = Annotated[int, Depends(require_admin)]
