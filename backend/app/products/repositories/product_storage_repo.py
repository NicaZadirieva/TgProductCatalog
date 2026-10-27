from typing import Annotated

from fastapi import Depends
from sqlalchemy import func, select

from app.products.model import Product
from app.shared.db import DbSessionDeps


class ProductStorageRepo:
    def __init__(self, db_session: DbSessionDeps):
        self.db_session = db_session

    async def save(self, product: Product) -> Product:
        self.db_session.add(product)
        await self.db_session.commit()
        await self.db_session.refresh(product)
        return product

    async def get_by_id(self, product_id: int):
        return await self.db_session.get(Product, product_id)

    async def get_batch(self, start: int, size: int) -> list[Product]:
        stmt = (
            select(Product)
            .order_by(Product.name.asc(), Product.id.asc())
            .limit(size)
            .offset(start)
        )
        res = await self.db_session.execute(stmt)
        return list(res.scalars())

    async def get_count(self) -> int | None:
        stmt = select(func.count()).select_from(Product)
        res = await self.db_session.execute(stmt)
        return res.scalar_one_or_none()


def get_product_storage_repo(db_session: DbSessionDeps):
    return ProductStorageRepo(db_session)


ProductStorageRepoDeps = Annotated[
    ProductStorageRepo, Depends(get_product_storage_repo)
]
