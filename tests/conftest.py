"""Shared pytest fixtures for API tests."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_settings

# Ensure app import sees required env vars during test collection.
os.environ.setdefault("STEAM_API_KEY", "test-api-key")
os.environ.setdefault("STEAM_ID_64", "76561198000000000")
os.environ.setdefault("ROOT_PATH", "")

from app.main import app


@pytest.fixture(autouse=True)
def test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide required environment variables for app settings in tests."""
    monkeypatch.setenv("STEAM_API_KEY", "test-api-key")
    monkeypatch.setenv("STEAM_ID_64", "76561198000000000")
    monkeypatch.setenv("ROOT_PATH", "")

    # Settings are cached with lru_cache, so clear between tests.
    get_settings.cache_clear()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create a test client with app lifespan handling enabled.

    Yields:
        TestClient: An initialized test client for API requests.
    """
    with TestClient(app) as test_client:
        yield test_client
