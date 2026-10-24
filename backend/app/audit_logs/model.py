import uuid
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


class LogLevel(PyEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"


class AuditLogs(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    instance_id: Mapped[str] = mapped_column(String(50), nullable=False)
    """
    TODO: Для указания, какой инстанс API сделал действие. Константа в .env внутри tg-bot и фронтенде
    """
    service: Mapped[str] = mapped_column(String(20), nullable=False)
    """
    Для указания названия сервиса (bot/backend/frontend), инициирующего действие
    """
    trace_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    request_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("update_telegram_requests.request_id")
    )
    update_id: Mapped[int] = mapped_column(
        ForeignKey("update_telegram_requests.update_id")
    )
    level: Mapped[LogLevel] = mapped_column(Enum(LogLevel), nullable=False)
    # например, product_created или product_photo_uploaded
    event: Mapped[str] = mapped_column(String(100), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
