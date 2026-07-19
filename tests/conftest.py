"""Shared pytest fixtures for API tests."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_settings
from app.main import app


@pytest.fixture(autouse=True)
def _test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide required environment variables for app settings in tests."""
    monkeypatch.setenv("STEAM_API_KEY", "test-api-key")
    monkeypatch.setenv("STEAM_ID_64", "76561198000000000")

    # Settings are cached with lru_cache, so clear between tests.
    get_settings.cache_clear()


@pytest.fixture
def client(_test_env: None) -> Generator[TestClient, None, None]:
    """Create a test client with app lifespan handling enabled.

    Args:
        _test_env: Ensures Steam credentials exist before lifespan runs.

    Yields:
        TestClient: An initialized test client for API requests.
    """
    with TestClient(app) as test_client:
        yield test_client
