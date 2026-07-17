"""Dependencies for the FastAPI application."""

from functools import lru_cache
from typing import Annotated

import aiohttp
from fastapi import Depends, Request
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    api_key: str = Field(validation_alias="STEAM_API_KEY")
    user_id: str = Field(validation_alias="STEAM_ID_64")
    root_path: str = Field(default="", validation_alias="ROOT_PATH")


def get_client(request: Request) -> aiohttp.ClientSession:
    """Get the aiohttp client session from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        aiohttp.ClientSession: The async HTTP client session.
    """
    return request.app.state.client


@lru_cache
def get_settings() -> Settings:
    """Get application settings. Cached using lru_cache.

    Returns:
        Settings: The application configuration settings.
    """
    return Settings()


ClientDependency = Annotated[aiohttp.ClientSession, Depends(get_client)]

SettingsDependency = Annotated[Settings, Depends(get_settings)]
