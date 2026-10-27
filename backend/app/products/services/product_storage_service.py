from http.client import HTTPException
from typing import Annotated

from fastapi import Depends

from app.products.model import Product
from app.products.schema import CreateProductRequest, GetProductsRequest
from app.products.services.admin_service import AdminServiceDeps

from ..repositories.product_storage_repo import ProductStorageRepoDeps


class ProductStorageService:
    def __init__(
        self,
        product_storage_repo: ProductStorageRepoDeps,
        admin_service: AdminServiceDeps,
    ):
        self.product_storage_repo = product_storage_repo
        self.admin_service = admin_service

    async def create_product(self, telegram_id: int, dto: CreateProductRequest):
        if self.admin_service.is_admin(telegram_id):
            product = Product(name=dto.name, photo_path=dto.photo_path)
            return await self.product_storage_repo.save(product)
        raise HTTPException(403, "Not corrected user. Must be admin")

    async def get_by_id(self, product_id: int):
        return await self.product_storage_repo.get_by_id(product_id)

    async def get_by_page(self, dto: GetProductsRequest):
        products = await self.product_storage_repo.get_batch(
            (dto.current_page - 1) * (dto.page_size), dto.page_size
        )
        count = await self.product_storage_repo.get_count() or 0
        return (products, count)


def get_product_storage_service(
    product_storage_repo: ProductStorageRepoDeps, admin_service: AdminServiceDeps
):
    return ProductStorageService(product_storage_repo, admin_service)


ProductStorageServiceDeps = Annotated[
    ProductStorageService, Depends(get_product_storage_service)
]
