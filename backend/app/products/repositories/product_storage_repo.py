from typing import Annotated

from fastapi import Depends

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


def get_product_storage_repo(db_session: DbSessionDeps):
    return ProductStorageRepo(db_session)


ProductStorageRepoDeps = Annotated[
    ProductStorageRepo, Depends(get_product_storage_repo)
]
