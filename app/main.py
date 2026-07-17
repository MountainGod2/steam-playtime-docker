"""FastAPI application initialization and routing setup."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from .dependencies import get_settings
from .routers import health, steam
from .version import __version__

LOGGER = logging.getLogger(__name__)

HTTP_TIMEOUT = aiohttp.ClientTimeout(total=5.0)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and teardown app resources.

    Args:
        app: The incoming FastAPI application instance.

    Yields:
        None: Yields control back to the application.
    """
    # Validate required environment variables eagerly so startup fails fast.
    get_settings()

    app.state.client = aiohttp.ClientSession(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.close()


settings = get_settings()

app = FastAPI(
    title="Steam Playtime API",
    version=__version__,
    lifespan=lifespan,
    root_path=settings.root_path,
)

app.include_router(health.router)
app.include_router(steam.router)
