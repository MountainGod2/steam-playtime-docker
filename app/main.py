"""FastAPI application initialization and routing setup."""

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from .dependencies import SteamSettings
from .routers import steam

LOGGER = logging.getLogger(__name__)
HTTP_TIMEOUT = httpx.Timeout(5.0)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and teardown app resources.

    Args:
        app: The incoming FastAPI application instance.

    Yields:
        None: Yields control back to the application.

    Raises:
        RuntimeError: If required environment variables are missing.
    """
    api_key = os.getenv("STEAM_API_KEY")
    user_id = os.getenv("STEAM_ID_64")

    if not api_key or not user_id:
        msg = "Missing STEAM_API_KEY or STEAM_ID_64"
        LOGGER.error(msg)
        raise RuntimeError(msg)

    app.state.settings = SteamSettings(api_key=api_key, user_id=user_id)
    app.state.client = httpx.AsyncClient(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.aclose()


root_path = os.getenv("ROOT_PATH", "")
app = FastAPI(
    title="Steam Playtime API",
    lifespan=lifespan,
    root_path=root_path,
)

app.include_router(steam.router)
