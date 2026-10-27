from datetime import datetime
from typing import Annotated
from fastapi import Depends, Path, Query
from pydantic import BaseModel, ConfigDict


# создание товара
class CreateProductRequest(BaseModel):
    name: str
    photo_path: str


class CreateProductResponse(BaseModel):
    product_id: int


# получение товара
class GetProductsRequest(BaseModel):
    current_page: int
    page_size: int


def get_products_query(
    current_page: int = Query(..., ge=1),
    page_size: int = Query(..., ge=1, le=100),
) -> GetProductsRequest:
    return GetProductsRequest(
        current_page=current_page,
        page_size=page_size,
    )


GetProductsQueryDeps = Annotated[GetProductsRequest, Depends(get_products_query)]


class ProductOut(BaseModel):
    id: int
    name: str
    photo_path: str


class GetProductsResponse(BaseModel):
    count: int
    items: list[ProductOut]


# получение фото товара по его id
class ProductPhotoResponse(BaseModel):
    product_id: int
    photo_link: str
    expires_at: datetime
