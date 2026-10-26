from typing import Annotated

from fastapi import Depends
from minio import Minio

from app.shared.settings import Settings

settings = Settings()  # type: ignore


def get_minio_client() -> Minio:
    return Minio(
        settings.minio.MINIO_API_URL,
        access_key=settings.minio.MINIO_ACCESS_KEY,
        secret_key=settings.minio.MINIO_SECRET_KEY,
        secure=settings.minio.MINIO_SECURE,
    )


MinioClientDeps = Annotated[Minio, Depends(get_minio_client)]
