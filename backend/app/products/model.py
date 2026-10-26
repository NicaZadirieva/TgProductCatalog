from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


class Product(Base):
    """
    Модель продукта в базе данных
    """

    __tablename__ = "products"

    # товаров может быть много => BigInteger
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # ~ 130 символов на продукт русскими буквами
    # TODO: спросить, уникально ли имя?
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    # products/{uuid}.{расширение}. Фото хранится в MinIO
    # TODO: протестировать сценарий база данных недоступна, но в MinIO есть изменения. Должен быть лог об этом
    photo_path: Mapped[str] = mapped_column(String(255), nullable=False)

    def __init__(self, name: str, photo_path: str):
        self.name = name
        self.photo_path = photo_path
