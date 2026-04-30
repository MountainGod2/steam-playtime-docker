"""Dependencies for the FastAPI application."""

from functools import lru_cache
from typing import Annotated

import aiohttp
from fastapi import Depends, Request
from pydantic import Field
from pydantic_settings import BaseSettings


class SteamSettings(BaseSettings):
    """Configuration for Steam API access."""

    api_key: str = Field(validation_alias="STEAM_API_KEY")
    user_id: str = Field(validation_alias="STEAM_ID_64")


def get_client(request: Request) -> aiohttp.ClientSession:
    """Get the aiohttp client session from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        aiohttp.ClientSession: The async HTTP client session.
    """
    return request.app.state.client


@lru_cache
def get_settings() -> SteamSettings:
    """Get the Steam settings. Cached using lru_cache.

    Returns:
        SteamSettings: The configuration settings.
    """
    return SteamSettings()  # ty:ignore[missing-argument]


ClientDependency = Annotated[aiohttp.ClientSession, Depends(get_client)]
"""aiohttp.ClientSession: Dependency for the aiohttp client session."""

SettingsDependency = Annotated[SteamSettings, Depends(get_settings)]
"""SteamSettings: Dependency for the Steam settings."""
