"""Display the total playtime using the Steam Web API."""

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from httpx import HTTPStatusError, RequestError, TimeoutException

LOGGER = logging.getLogger(__name__)
HTTP_TIMEOUT = httpx.Timeout(5.0)

STEAM_OWNED_GAMES_URL = (
    "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
)


@dataclass(frozen=True)
class SteamSettings:
    """Configuration for Steam API access."""

    api_key: str
    user_id: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Initialize and teardown app resources.

    Raises:
        RuntimeError: If required environment variables are missing.
    """
    api_key = os.getenv("STEAM_API_KEY")
    user_id = os.getenv("STEAM_ID_64")

    if not api_key or not user_id:
        msg = "Missing STEAM_API_KEY or STEAM_ID_64"
        LOGGER.error(msg)
        raise RuntimeError(msg)

    app.state.settings = SteamSettings(api_key=api_key, user_id=user_id)
    app.state.client = httpx.AsyncClient(timeout=HTTP_TIMEOUT)

    try:
        yield
    finally:
        await app.state.client.aclose()


app = FastAPI(title="Steam Playtime API", lifespan=lifespan)


async def get_steam_stats() -> dict[str, Any]:
    """Fetch Steam-owned games and calculate total playtime.

    Returns:
        dict: Total games and total playtime in minutes and hours.

    Raises:
        TypeError: If the Steam API response has an unexpected shape.
    """
    client: httpx.AsyncClient = app.state.client
    settings: SteamSettings = app.state.settings
    params = {
        "key": settings.api_key,
        "steamid": settings.user_id,
        "format": "json",
        "include_appinfo": 1,
    }

    response = await client.get(STEAM_OWNED_GAMES_URL, params=params)
    response.raise_for_status()
    data = response.json()
    response_data = data.get("response")
    if not isinstance(response_data, dict):
        msg = "Steam API response missing 'response' field"
        raise TypeError(msg)

    games = response_data.get("games", [])
    if not isinstance(games, list):
        msg = "Steam API response 'games' field is not a list"
        raise TypeError(msg)

    total_playtime_minutes = sum(
        game.get("playtime_forever", 0) for game in games
    )

    return {
        "total_games": len(games),
        "total_playtime_forever_minutes": total_playtime_minutes,
        "total_playtime_forever_hours": round(total_playtime_minutes / 60, 1),
    }


@app.get("/steam-stats")
async def steam_stats() -> dict[str, Any]:
    """API endpoint to return Steam stats.

    Returns:
        dict: Steam stats including total games and playtime.

    Raises:
        HTTPException: For Steam API errors or invalid responses.
    """
    try:
        return await get_steam_stats()

    except TimeoutException:
        msg = "Steam API request timed out"
        raise HTTPException(504, detail=msg) from None

    except HTTPStatusError as e:
        msg = f"Steam API returned status {e.response.status_code}"
        raise HTTPException(502, detail=msg) from e

    except RequestError as e:
        msg = "Failed to reach Steam API"
        raise HTTPException(502, detail=msg) from e

    except TypeError as e:
        msg = f"Invalid Steam API response: {e}"
        raise HTTPException(502, detail=msg) from e
