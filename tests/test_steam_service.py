"""Service-layer tests for Steam API integration behavior."""

import asyncio
import re

import aiohttp
import pytest
from aioresponses import aioresponses

from app.dependencies import get_settings
from app.exceptions import AppHTTPError
from app.schemas.steam import SteamStatsResponse
from app.services.steam import STEAM_OWNED_GAMES_URL, get_steam_stats

STEAM_URL_PATTERN = re.compile(rf"{re.escape(STEAM_OWNED_GAMES_URL)}.*")


async def _fetch_stats() -> SteamStatsResponse:
    """Execute one service request with a short-lived aiohttp session.

    Returns:
        SteamStatsResponse: The service response for steam stats.
    """
    async with aiohttp.ClientSession() as session:
        return await get_steam_stats(session, get_settings())


def test_get_steam_stats_returns_aggregated_totals() -> None:
    """Returns total counts and playtime for a valid upstream payload."""
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

        response = asyncio.run(_fetch_stats())

    assert response.model_dump() == {
        "total_games": 3,
        "total_playtime_forever_minutes": 150,
        "total_playtime_forever_hours": 2.5,
    }


@pytest.mark.parametrize(
    ("payload", "status_code", "detail"),
    [
        ({"unexpected": {}}, 502, "Steam API returned an invalid response"),
        ({"response": {}}, 502, "Steam API returned an invalid response"),
    ],
)
def test_get_steam_stats_maps_invalid_payload_errors(
    payload: object, status_code: int, detail: str
) -> None:
    """Raises AppHTTPError for structurally invalid upstream payloads."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, payload=payload, status=200)

        with pytest.raises(AppHTTPError) as error_info:
            asyncio.run(_fetch_stats())

    assert error_info.value.status_code == status_code
    assert error_info.value.detail == detail


def test_get_steam_stats_maps_upstream_http_error() -> None:
    """Raises AppHTTPError when upstream responds with non-2xx status."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, status=503)

        with pytest.raises(AppHTTPError) as error_info:
            asyncio.run(_fetch_stats())

    assert error_info.value.status_code == 502
    assert error_info.value.detail == "Steam API returned status 503"


def test_get_steam_stats_maps_timeout_error() -> None:
    """Raises AppHTTPError when the upstream request times out."""
    with aioresponses() as mocked:
        mocked.get(STEAM_URL_PATTERN, exception=TimeoutError())

        with pytest.raises(AppHTTPError) as error_info:
            asyncio.run(_fetch_stats())

    assert error_info.value.status_code == 504
    assert error_info.value.detail == "Steam API request timed out"


def test_get_steam_stats_maps_connection_error() -> None:
    """Raises AppHTTPError when the upstream host cannot be reached."""
    with aioresponses() as mocked:
        mocked.get(
            STEAM_URL_PATTERN,
            exception=aiohttp.ClientConnectionError("connection failed"),
        )

        with pytest.raises(AppHTTPError) as error_info:
            asyncio.run(_fetch_stats())

    assert error_info.value.status_code == 502
    assert error_info.value.detail == "Failed to reach Steam API"
