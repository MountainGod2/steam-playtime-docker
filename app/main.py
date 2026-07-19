"""FastAPI application initialization and routing setup."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from .dependencies import Settings, get_settings
from .routers import health, steam
from .version import __version__

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


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application instance.

    Args:
        settings: Optional settings instance.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    resolved_settings = settings or get_settings()

    application = FastAPI(
        title="Steam Playtime API",
        version=__version__,
        lifespan=lifespan,
        root_path=resolved_settings.root_path,
    )

    application.include_router(health.router)
    application.include_router(steam.router)

    return application


app = create_app()
