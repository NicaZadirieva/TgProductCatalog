from urllib.parse import urlparse

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonAppSettings(BaseModel):
    ENVIRONMENT: str = (
        "development"  # TODO: настроить логи для development и production
    )
    BACKEND_URL: str
    MINI_APP_URL: str


class TgAppSettings(BaseModel):
    TELEGRAM_BOT_TOKEN: str


class WebhookSettings(BaseModel):
    WEBHOOK_HOST: str
    WEBAPP_HOST: str
    WEBAPP_PORT: int


class Settings(BaseSettings):
    # Common
    ENVIRONMENT: str = "development"
    MINI_APP_URL: str
    # Telegram
    TELEGRAM_BOT_TOKEN: str

    # Backend (api)
    BACKEND_URL: str

    # Webhook
    WEBHOOK_HOST: str
    WEBAPP_HOST: str
    WEBAPP_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        allowed = {"development", "production"}
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v

    @field_validator("WEBAPP_PORT")
    @classmethod
    def validate_webapp_port(cls, v: int) -> int:
        allowed = {443, 80, 8080, 88, 8443}
        if v not in allowed:
            raise ValueError(f"WEBAPP_PORT must be one of {allowed}")
        return v

    @field_validator("BACKEND_URL")
    @classmethod
    def validate_backend_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.hostname:
            raise ValueError("BACKEND_URL must have hostname")
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("BACKEND_URL port must be 1...65535")
        return v

    @field_validator("MINI_APP_URL")
    @classmethod
    def validate_miniapp_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.hostname:
            raise ValueError("MINI_APP_URL must have hostname")
        if parsed.scheme != "https":
            raise ValueError("MINI_APP_URL must be secured")
        if parsed.port is not None and not (1 <= parsed.port <= 65535):
            raise ValueError("MINI_APP_URL port must be 1...65535")
        return v

    @property
    def common_app(self) -> CommonAppSettings:
        return CommonAppSettings(
            ENVIRONMENT=self.ENVIRONMENT,
            BACKEND_URL=self.BACKEND_URL,
            MINI_APP_URL=self.MINI_APP_URL,
        )

    @property
    def tg_app(self) -> TgAppSettings:
        return TgAppSettings(TELEGRAM_BOT_TOKEN=self.TELEGRAM_BOT_TOKEN)

    @property
    def webhook(self) -> WebhookSettings:
        return WebhookSettings(
            WEBAPP_HOST=self.WEBAPP_HOST,
            WEBHOOK_HOST=self.WEBHOOK_HOST,
            WEBAPP_PORT=self.WEBAPP_PORT,
        )


settings = Settings()  # type:ignore[call-arg]
