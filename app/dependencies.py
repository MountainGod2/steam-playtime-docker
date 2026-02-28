"""Dependencies for the FastAPI application."""

from dataclasses import dataclass
from typing import Annotated

import httpx
from fastapi import Depends, Request


@dataclass(frozen=True)
class SteamSettings:
    """Configuration for Steam API access."""

    api_key: str
    user_id: str


def get_client(request: Request) -> httpx.AsyncClient:
    """Get the HTTPX client from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        httpx.AsyncClient: The async HTTP client.
    """
    return request.app.state.client


def get_settings(request: Request) -> SteamSettings:
    """Get the Steam settings from the application state.

    Args:
        request: The incoming FastAPI request.

    Returns:
        SteamSettings: The configuration settings.
    """
    return request.app.state.settings


ClientDependency = Annotated[httpx.AsyncClient, Depends(get_client)]
SettingsDependency = Annotated[SteamSettings, Depends(get_settings)]
