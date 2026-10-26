import logging
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.middleware.is_admin import AdminUserIdDeps
from app.products.schema import (
    CreateProductRequest,
    CreateProductResponse,
    GetProductsQueryDeps,
    GetProductsResponse,
    ProductOut,
    ProductPhotoResponse,
)
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


@router.get("/", response_model=GetProductsResponse, status_code=200)
async def get_by_page(
    dto: GetProductsQueryDeps, product_storage_service: ProductStorageServiceDeps
):
    products, count = await product_storage_service.get_by_page(dto)
    return GetProductsResponse(
        count=count,
        items=[
            ProductOut(name=product.name, id=product.id, photo_path=product.photo_path)
            for product in products
        ],
    )


@router.get("/{product_id}/image", status_code=200, response_model=ProductPhotoResponse)
async def get_product_image(
    product_id: int,
    product_storage_service: ProductStorageServiceDeps,
    product_bucket_service: MinioProductBucketServiceDeps,
):
    product = await product_storage_service.get_by_id(product_id)
    if product is None:
        raise HTTPException(404, "Товар с переданным id не найден")
    file_bucket_url = await product_bucket_service.get_image_url_by_key(
        product.photo_path
    )
    return ProductPhotoResponse(
        product_id=product.id,
        photo_link=file_bucket_url.url,
        expires_at=file_bucket_url.expires_at,
    )
