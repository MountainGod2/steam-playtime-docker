"""Application configuration models loaded from environment variables."""

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class _EnvironmentSettings(BaseSettings):
    """Base settings configuration shared by application settings models."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


class RootPathSettings(_EnvironmentSettings):
    """Settings required while constructing the FastAPI application."""

    root_path: str = Field(default="", validation_alias="ROOT_PATH")


class Settings(RootPathSettings):
    """Steam API configuration loaded from environment variables."""

    steam_api_key: SecretStr = Field(validation_alias="STEAM_API_KEY")
    steam_id_64: str = Field(validation_alias="STEAM_ID_64")
