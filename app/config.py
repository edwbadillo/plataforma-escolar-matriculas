import logging

from pydantic_settings import BaseSettings

logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    """App settings."""

    DEBUG: bool = False
    ENV: str = "local"
    DATABASE_URL: str = ""


settings = Settings()
