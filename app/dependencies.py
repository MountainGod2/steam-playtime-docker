"""Dependencies for the FastAPI application."""

from functools import lru_cache
from typing import Annotated

import aiohttp
from fastapi import Depends, Request
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


def get_client(request: Request) -> aiohttp.ClientSession:
    """Get the aiohttp client session from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        The shared aiohttp client session.
    """
    return request.app.state.client


@lru_cache
def get_settings() -> Settings:
    """Load and cache the Steam API configuration.

    Returns:
        The application configuration settings.
    """
    return Settings()


ClientDependency = Annotated[aiohttp.ClientSession, Depends(get_client)]
SettingsDependency = Annotated[Settings, Depends(get_settings)]
