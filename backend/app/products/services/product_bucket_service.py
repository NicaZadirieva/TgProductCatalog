import os
import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, UploadFile

from app.products.services.admin_service import AdminServiceDeps
from app.shared.file_bucket_url import FileBucketUrl
from app.shared.settings import Settings

from ..repositories.minio_product_bucket_repo import MinioProductBucketRepoDeps

settings = Settings()  # type: ignore


class ProductBucketService:
    """
    Сервис для работы с изображениями, хранящимися в MinIO
    """

    def __init__(
        self,
        minio_product_repo: MinioProductBucketRepoDeps,
        admin_service: AdminServiceDeps,
    ):
        self.minio_product_repo = minio_product_repo
        self.admin_service = admin_service

    def __generate_image_key__(self, filename: str):
        extension = os.path.splitext(filename)[1]
        return f"{uuid.uuid4().hex}{extension}"

    def __is_image__(self, file: UploadFile):
        return not file.content_type or not file.content_type.startswith("image/")

    async def upload_image(self, telegram_id: int, file: UploadFile):
        if self.admin_service.is_admin(telegram_id):
            if not self.__is_image__(file):
                raise HTTPException(415, "Только изображения разрешены")
            if not file.filename:
                raise HTTPException(422, "Укажите имя файла")
            object_key = self.__generate_image_key__(file.filename)
            return await self.minio_product_repo.save(object_key, file)
        raise ValueError("Not corrected user. Must be admin")

    def get_image_url_by_key(self, object_key: str) -> FileBucketUrl:
        return self.minio_product_repo.get(object_key)


def get_minio_service(
    minio_product_repo: MinioProductBucketRepoDeps, admin_service: AdminServiceDeps
):
    return ProductBucketService(minio_product_repo, admin_service)


MinioProductBucketServiceDeps = Annotated[
    ProductBucketService, Depends(get_minio_service)
]
