import os
import uuid

from fastapi import HTTPException, UploadFile

from app.shared.file_bucket_url import FileBucketUrl
from app.shared.settings import Settings

from ..repositories.minio_product_bucket_repo import MinioProductBucketRepoDeps

settings = Settings()  # type: ignore


class ProductBucketService:
    """
    Сервис для работы с изображениями, хранящимися в MinIO
    """

    def __init__(self, minio_product_repo: MinioProductBucketRepoDeps):
        self.minio_product_repo = minio_product_repo

    def __generate_image_key__(self, filename: str):
        extension = os.path.splitext(filename)[1]
        return f"products/{uuid.uuid4().hex}{extension}"

    def __is_image__(self, file: UploadFile):
        return not file.content_type or not file.content_type.startswith("image/")

    async def upload_image(self, file: UploadFile):
        if not self.__is_image__(file):
            raise HTTPException(415, "Только изображения разрешены")
        if not file.filename:
            raise HTTPException(422, "Укажите имя файла")
        object_key = self.__generate_image_key__(file.filename)
        await self.minio_product_repo.save(object_key, file)

    def get_image_url_by_key(self, object_key: str) -> FileBucketUrl:
        return self.minio_product_repo.get(object_key)
