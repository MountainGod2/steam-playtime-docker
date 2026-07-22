"""Dependencies for the FastAPI application."""

from functools import lru_cache
from typing import Annotated

import aiohttp
from fastapi import Depends, Request

from app.config import Settings


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
