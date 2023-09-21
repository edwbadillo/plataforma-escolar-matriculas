import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    """App settings."""

    DEBUG: bool = False
    ENV: str = "local"
    DATABASE_URL: str = ""

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
