from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile

router = APIRouter(prefix="/v1/product", tags=["Products"])


@router.post("/create")
async def create_product(
    name: Annotated[str, Form(max_length=255, description="Название товара")],
    original_photo: Annotated[UploadFile, File(description="Оригинальное изображение")],
):
    pass
