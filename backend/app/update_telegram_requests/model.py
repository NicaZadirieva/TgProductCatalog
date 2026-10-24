from datetime import datetime
import uuid
from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Uuid
from app.shared.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class UpdateTelegramRequest(Base):
    """
    обработанные запросы от telegram
    (решает проблему дублей при создании товаров
    из-за особенностей обработки запросов
    под капотом telegram)
    """

    __tablename__ = "update_telegram_requests"

    update_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    """
    id обработки сообщения, первичный ключ, задаваемый телеграммом
    """
    request_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False, unique=True)
    """
    id для запроса. генерируется кодом через uuid
    """
    trace_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    # (для чистки старых записей этой таблицы)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    """
    поле для обозначения времени, когда запрос обработан. Например, товар добавился
    """
    processed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
