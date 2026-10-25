from typing import Annotated

from fastapi import Depends
from app.products.model import Product
from app.products.schema import CreateProductRequest
from ..repositories.product_storage_repo import ProductStorageRepoDeps


class ProductStorageService:
    def __init__(self, product_storage_repo: ProductStorageRepoDeps):
        self.product_storage_repo = product_storage_repo

    async def create_product(self, dto: CreateProductRequest):
        product = Product(name=dto.name, photo_path=dto.photo_path)
        return await self.product_storage_repo.save(product)


def get_product_storage_service(product_storage_repo: ProductStorageRepoDeps):
    return ProductStorageService(product_storage_repo)


ProductStorageServiceDeps = Annotated[
    ProductStorageService, Depends(get_product_storage_service)
]
