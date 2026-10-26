import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from app.middleware.is_admin import AdminUserIdDeps
from app.products.schema import CreateProductRequest, CreateProductResponse
from app.products.services.product_bucket_service import MinioProductBucketServiceDeps
from app.products.services.product_storage_service import ProductStorageServiceDeps

router = APIRouter(prefix="/v1/product", tags=["Products"])

logger = logging.getLogger(__name__)


@router.post("/create", response_model=CreateProductResponse, status_code=201)
async def create_product(
    telegram_id: AdminUserIdDeps,
    name: Annotated[str, Form(max_length=255, description="Название товара")],
    original_photo: Annotated[UploadFile, File(description="Оригинальное изображение")],
    photo_extension: Annotated[
        str, Form(max_length=255, description="Расширение файла")
    ],
    product_bucket_service: MinioProductBucketServiceDeps,
    product_storage_service: ProductStorageServiceDeps,
):
    try:
        # Сначала сохраняем изображение, чтобы в базе не хранились битые ссылки
        photo_path = await product_bucket_service.upload_image(
            telegram_id, original_photo, photo_extension
        )
        # При успешном сохранении записываем в базу
        dto = CreateProductRequest(name=name, photo_path=photo_path)
        new_product = await product_storage_service.create_product(telegram_id, dto)
        return CreateProductResponse(product_id=new_product.id)
    except:
        logger.error(
            "Неуспешная попытка создать запись о товаре",
            extra={"telegram_id": telegram_id},
        )
        raise
