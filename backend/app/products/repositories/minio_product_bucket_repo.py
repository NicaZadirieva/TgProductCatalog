from datetime import timedelta
import logging
from typing import Annotated, Any

from fastapi import Depends, HTTPException
from minio import Minio, S3Error

from app.shared.file_bucket_url import FileBucketUrl
from app.shared.settings import Settings

settings = Settings()  # type: ignore

logger = logging.getLogger(__name__)


class MinioProductBucketRepository:
    def __init__(self, minio_client: Minio):
        self.minio_client = minio_client

    def create_bucket_if_not_exists(self):
        try:
            if not self.minio_client.bucket_exists(settings.minio.PRODUCT_BUCKET_NAME):
                self.minio_client.make_bucket(settings.minio.PRODUCT_BUCKET_NAME)
        except S3Error as e:
            logger.error("Ошибка при создании бакета", exc_info=e)
            raise

    async def save(self, key: str, file: Any):
        try:
            self.minio_client.put_object(
                bucket_name=settings.minio.PRODUCT_BUCKET_NAME,
                object_name=key,
                data=file.file,
                length=-1,
                content_type=file.content_type,
            )
            return key
        except S3Error as e:
            logger.error(
                "Ошибка при сохранении в MinIO", exc_info=e, extra={"key": key}
            )
            raise HTTPException(500, f"Ошибка при сохранении в MinIO: {e}")
        finally:
            await file.close()

    def get(self, key: str) -> FileBucketUrl:
        try:
            url = self.minio_client.presigned_get_object(
                settings.minio.PRODUCT_BUCKET_NAME,
                key,
                expires=timedelta(minutes=settings.minio.PRODUCT_LINK_EXPIRES_MINUTES),
            )
            return FileBucketUrl(url=url)
        except S3Error as e:
            logger.error(
                "Не удалось создать ссылку на файл", exc_info=e, extra={"key": key}
            )
            raise HTTPException(500, f"Не удалось создать ссылку на файл: {e}")


def get_minio_product_repo(minio_client: Minio):
    return MinioProductBucketRepository(minio_client)


MinioProductBucketRepoDeps = Annotated[
    MinioProductBucketRepository, Depends(get_minio_product_repo)
]
