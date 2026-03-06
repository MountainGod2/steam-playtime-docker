"""Dependencies for the FastAPI application."""

from functools import lru_cache
from typing import Annotated

import httpx
from fastapi import Depends, Request
from pydantic import Field
from pydantic_settings import BaseSettings


class SteamSettings(BaseSettings):
    """Configuration for Steam API access."""

    api_key: str = Field(validation_alias="STEAM_API_KEY")
    user_id: str = Field(validation_alias="STEAM_ID_64")


def get_client(request: Request) -> httpx.AsyncClient:
    """Get the HTTPX client from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        httpx.AsyncClient: The async HTTP client.
    """
    return request.app.state.client


@lru_cache
def get_settings() -> SteamSettings:
    """Get the Steam settings. Cached using lru_cache.

    Returns:
        SteamSettings: The configuration settings.
    """
    return SteamSettings()


ClientDependency = Annotated[httpx.AsyncClient, Depends(get_client)]
"""httpx.AsyncClient: Dependency for the HTTPX async client."""

SettingsDependency = Annotated[SteamSettings, Depends(get_settings)]
"""SteamSettings: Dependency for the Steam settings."""
