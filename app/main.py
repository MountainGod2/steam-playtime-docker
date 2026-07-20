"""FastAPI application initialization and routing setup."""

from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI

from .dependencies import RootPathSettings, Settings, get_settings
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
    if not hasattr(app.state, "settings"):
        app.state.settings = get_settings()

    app.state.client = aiohttp.ClientSession(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.close()


def _settings_provider(settings: Settings) -> Callable[[], Settings]:
    """Create a dependency provider for supplied settings.

    Args:
        settings: The settings instance to provide.

    Returns:
        A callable that returns the supplied settings.
    """

    def provide_settings() -> Settings:
        """Return the injected settings instance for dependency override."""
        return settings

    return provide_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        settings: Optional complete settings instance, primarily for embedding
            or tests. Required Steam credentials remain deferred until startup
            when this argument is omitted.

    Returns:
        The configured FastAPI application.
    """
    root_path = (
        settings.root_path
        if settings is not None
        else RootPathSettings().root_path
    )

    application = FastAPI(
        title="Steam Playtime API",
        version=__version__,
        lifespan=lifespan,
        root_path=root_path,
    )

    if settings is not None:
        application.state.settings = settings
        application.dependency_overrides[get_settings] = _settings_provider(
            settings
        )

    application.include_router(health.router)
    application.include_router(steam.router)

    return application


app = create_app()
