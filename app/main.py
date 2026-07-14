"""FastAPI application initialization and routing setup."""

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from .dependencies import get_settings
from .routers import health, steam
from .version import __version__

LOGGER = logging.getLogger(__name__)
"""logging.Logger: Logger instance for the application."""

HTTP_TIMEOUT = aiohttp.ClientTimeout(total=5.0)
"""aiohttp.ClientTimeout: Timeout for HTTP requests, set to 5 seconds."""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and teardown app resources.

    Args:
        app: The incoming FastAPI application instance.

    Yields:
        None: Yields control back to the application.
    """
    get_settings()

    app.state.client = aiohttp.ClientSession(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.close()


root_path = os.getenv("ROOT_PATH", "")
"""str: Optional root path, set via the ROOT_PATH environment variable."""

app = FastAPI(
    title="Steam Playtime API",
    version=__version__,
    lifespan=lifespan,
    root_path=root_path,
)
"""FastAPI: The main FastAPI application instance."""

app.include_router(health.router)
app.include_router(steam.router)
