"""FastAPI application initialization and routing setup."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from .dependencies import RootPathSettings, get_settings
from .routers import health, steam
from .version import __version__

HTTP_TIMEOUT = aiohttp.ClientTimeout(total=5.0)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize and tear down application resources.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control to the running application.
    """
    app.state.settings = get_settings()
    app.state.client = aiohttp.ClientSession(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.close()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        The configured FastAPI application.
    """
    application = FastAPI(
        title="Steam Playtime API",
        version=__version__,
        lifespan=lifespan,
        root_path=RootPathSettings().root_path,
    )

    application.include_router(health.router)
    application.include_router(steam.router)

    return application


app = create_app()
