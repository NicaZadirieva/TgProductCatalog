from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonAppSettings(BaseModel):
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str
    TELEGRAM_ADMIN_IDS: list[int] = []

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "production"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    @field_validator("FRONTEND_URL")
    @classmethod
    def validate_frontend_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.hostname:
            raise ValueError("FRONTEND_URL must have hostname")
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("FRONTEND_URL port must be 1...65535")
        return v


class MinioSettings(BaseModel):
    MINIO_API_URL: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool

    PRODUCT_BUCKET_NAME: str
    PRODUCT_LINK_EXPIRES_MINUTES: int

    @field_validator("MINIO_API_URL")
    @classmethod
    def validate_minio_api_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.hostname:
            raise ValueError("MINIO_API_URL must have hostname")
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("MINIO_API_URL port must be 1...65535")
        return v


class DatabaseSettings(BaseModel):
    DATABASE_URL: str = Field(..., min_length=10, description="Database connection URL")
    DATABASE_URL_SYNC: str = Field(
        ..., min_length=10, description="Database connection sync URL"
    )

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if parsed.scheme not in {"postgresql", "postgresql+asyncpg"}:
            raise ValueError(
                "Database_url scheme must be postgresql or postgresql+asyncpg"
            )
        if not parsed.hostname:
            raise ValueError("Database_url must include hostname")

        dbname = (parsed.path or "").lstrip("/")
        if not dbname:
            raise ValueError("Database_url must include database")

        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("Database_url port must be 1...65535")

        return v


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., min_length=10)
    DATABASE_URL_SYNC: str = Field(..., min_length=10)

    # Common
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str
    TELEGRAM_ADMIN_IDS: list[int] = []

    # MinIo
    MINIO_API_URL: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_SECURE: bool

    PRODUCT_BUCKET_NAME: str
    PRODUCT_LINK_EXPIRES_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def common_app(self) -> CommonAppSettings:
        return CommonAppSettings(
            ENVIRONMENT=self.ENVIRONMENT,
            FRONTEND_URL=self.FRONTEND_URL,
            TELEGRAM_ADMIN_IDS=self.TELEGRAM_ADMIN_IDS,
        )

    @property
    def db(self) -> DatabaseSettings:
        return DatabaseSettings(
            DATABASE_URL=self.DATABASE_URL, DATABASE_URL_SYNC=self.DATABASE_URL_SYNC
        )

    @property
    def minio(self) -> MinioSettings:
        return MinioSettings(
            MINIO_ACCESS_KEY=self.MINIO_ACCESS_KEY,
            MINIO_SECRET_KEY=self.MINIO_SECRET_KEY,
            PRODUCT_BUCKET_NAME=self.PRODUCT_BUCKET_NAME,
            PRODUCT_LINK_EXPIRES_MINUTES=self.PRODUCT_LINK_EXPIRES_MINUTES,
            MINIO_API_URL=self.MINIO_API_URL,
            MINIO_SECURE=self.MINIO_SECURE,
        )


settings = Settings()  # type:ignore[call-arg]
