"""API endpoint tests."""

import re

import aiohttp
import pytest
from aioresponses import aioresponses
from fastapi.testclient import TestClient

STEAM_URL_PATTERN = re.compile(r"https://api\.steampowered\.com/.*/GetOwnedGames/v0001/.*")


def test_health_returns_ok(client: TestClient) -> None:
    """Returns 200 and an ok status payload for the health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_steam_stats_returns_aggregated_totals(client: TestClient) -> None:
    """Aggregates playtime values and returns totals for a valid payload."""
    payload = {
        "response": {
            "games": [
                {"playtime_forever": 120},
                {"playtime_forever": 30},
                {},
            ]
        }
    }

    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, payload=payload, status=200)

        response = client.get("/steam-stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_games": 3,
        "total_playtime_forever_minutes": 150,
        "total_playtime_forever_hours": 2.5,
    }


def test_steam_stats_returns_zero_for_empty_library(
    client: TestClient,
) -> None:
    """Returns zero totals when the Steam library has no games."""
    with aioresponses() as mocked:
        mocked.get(
            STEAM_URL_PATTERN,
            payload={"response": {"games": []}},
            status=200,
        )

        response = client.get("/steam-stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_games": 0,
        "total_playtime_forever_minutes": 0,
        "total_playtime_forever_hours": 0.0,
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"unexpected": {}},
        {"response": {}},
        {"response": {"games": None}},
        {"response": {"games": [None]}},
        {"response": {"games": [{"playtime_forever": -1}]}},
        {"response": {"games": [{"playtime_forever": "invalid"}]}},
    ],
)
def test_steam_stats_returns_502_for_invalid_payload(
    client: TestClient,
    payload: object,
) -> None:
    """Maps structurally invalid Steam payloads to a 502 response."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, payload=payload, status=200)

        response = client.get("/steam-stats")

    assert response.status_code == 502
    assert response.json() == {"detail": "Steam API returned an invalid response"}


def test_steam_stats_returns_502_for_invalid_json(
    client: TestClient,
) -> None:
    """Returns 502 when upstream responds with invalid JSON."""
    with aioresponses() as mocked:
        mocked.get(
            STEAM_URL_PATTERN,
            body="not-json",
            content_type="application/json",
            status=200,
        )

        response = client.get("/steam-stats")

    assert response.status_code == 502
    assert response.json() == {"detail": "Steam API returned an invalid response"}


def test_steam_stats_returns_502_for_upstream_http_error(
    client: TestClient,
) -> None:
    """Converts upstream non-2xx HTTP status codes into a 502 response."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, status=503)

        response = client.get("/steam-stats")

    assert response.status_code == 502
    assert response.json() == {"detail": "Steam API returned status 503"}


def test_steam_stats_returns_504_for_timeout(client: TestClient) -> None:
    """Returns 504 when the Steam API request times out."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, exception=TimeoutError())

        response = client.get("/steam-stats")

    assert response.status_code == 504
    assert response.json() == {"detail": "Steam API request timed out"}


def test_steam_stats_returns_502_for_connection_error(
    client: TestClient,
) -> None:
    """Returns 502 when the Steam API cannot be reached."""
    with aioresponses() as mocked:
        mocked.get(
            STEAM_URL_PATTERN,
            exception=aiohttp.ClientConnectionError("connection failed"),
        )

        response = client.get("/steam-stats")

    assert response.status_code == 502
    assert response.json() == {"detail": "Failed to reach Steam API"}
