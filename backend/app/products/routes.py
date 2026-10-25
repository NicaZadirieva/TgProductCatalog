from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

from app.products.schema import CreateProductRequest, CreateProductResponse
from app.products.services.product_bucket_service import MinioProductBucketServiceDeps
from app.products.services.product_storage_service import ProductStorageServiceDeps

router = APIRouter(prefix="/v1/product", tags=["Products"])


@router.post("/create", response_model=CreateProductResponse, status_code=201)
async def create_product(
    name: Annotated[str, Form(max_length=255, description="Название товара")],
    original_photo: Annotated[UploadFile, File(description="Оригинальное изображение")],
    product_bucket_service: MinioProductBucketServiceDeps,
    product_storage_service: ProductStorageServiceDeps,
):
    # Сначала сохраняем изображение, чтобы в базе не хранились битые ссылки
    photo_path = await product_bucket_service.upload_image(original_photo)
    # При успешном сохранении записываем в базу
    dto = CreateProductRequest(name=name, photo_path=photo_path)
    new_product = await product_storage_service.create_product(dto)
    return CreateProductResponse(product_id=new_product.id)
