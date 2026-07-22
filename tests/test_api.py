"""API endpoint tests."""

import logging
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.exceptions import AppHTTPError
from app.main import app
from app.schemas.steam import SteamStatsResponse


def test_health_returns_ok(client: TestClient) -> None:
    """Returns 200 and an ok status payload for the health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_steam_stats_returns_service_payload(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Returns whatever payload the service returns for a successful call."""
    expected = SteamStatsResponse(
        total_games=3,
        total_playtime_forever_minutes=150,
        total_playtime_forever_hours=2.5,
    )

    monkeypatch.setattr(
        "app.routers.steam.get_steam_stats",
        AsyncMock(return_value=expected),
    )

    response = client.get("/steam-stats")

    assert response.status_code == 200
    assert response.json() == expected.model_dump()


@pytest.mark.parametrize(
    ("raised_error", "expected_status", "expected_detail"),
    [
        (AppHTTPError(504, "Steam API request timed out"), 504, "Steam API request timed out"),
        (AppHTTPError(502, "Failed to reach Steam API"), 502, "Failed to reach Steam API"),
    ],
)
def test_steam_stats_maps_service_http_errors(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    raised_error: AppHTTPError,
    expected_status: int,
    expected_detail: str,
) -> None:
    """Maps service-level AppHTTPError exceptions into HTTP responses."""
    monkeypatch.setattr(
        "app.routers.steam.get_steam_stats",
        AsyncMock(side_effect=raised_error),
    )

    response = client.get("/steam-stats")

    assert response.status_code == expected_status
    assert response.json() == {"detail": expected_detail}


def test_unhandled_exception_returns_json_500_and_is_logged(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Returns a consistent JSON 500 response and logs unexpected errors."""

    def _raise_unexpected_error(*_args: object, **_kwargs: object) -> None:
        msg = "boom"
        raise KeyError(msg)

    monkeypatch.setattr("app.routers.steam.get_steam_stats", _raise_unexpected_error)
    caplog.set_level(logging.ERROR, logger="app.error_handlers")

    with TestClient(app, raise_server_exceptions=False) as test_client:
        response = test_client.get("/steam-stats")

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert "Unhandled exception while processing request" in caplog.text
    assert "KeyError: 'boom'" in caplog.text
