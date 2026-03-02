"""Steam specific endpoints."""

import httpx
from fastapi import APIRouter, HTTPException
from httpx import HTTPStatusError, RequestError, TimeoutException
from pydantic import BaseModel

from app.dependencies import ClientDependency, SettingsDependency, SteamSettings

router = APIRouter()
"""router: APIRouter instance for Steam-related endpoints."""

STEAM_OWNED_GAMES_URL = (
    "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
)
"""STEAM_OWNED_GAMES_URL: URL for fetching Steam-owned games."""


class SteamStatsResponse(BaseModel):
    """Response model for Steam statistics."""

    total_games: int
    total_playtime_forever_minutes: int
    total_playtime_forever_hours: float


async def get_steam_stats(
    client: httpx.AsyncClient, settings: SteamSettings
) -> SteamStatsResponse:
    """Fetch Steam-owned games and calculate total playtime.

    Args:
        client: The HTTPX async client to use.
        settings: The Steam API settings containing user and key.

    Returns:
        dict: Total games and total playtime in minutes and hours.

    Raises:
        TypeError: If the Steam API response has an unexpected shape.
    """
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

    return SteamStatsResponse(
        total_games=len(games),
        total_playtime_forever_minutes=total_playtime_minutes,
        total_playtime_forever_hours=round(total_playtime_minutes / 60, 1),
    )


@router.get("/steam-stats", tags=["steam"])
async def steam_stats(
    client: ClientDependency, settings: SettingsDependency
) -> SteamStatsResponse:
    """API endpoint to return Steam stats.

    Args:
        client: The injected HTTPX async client dependency.
        settings: The injected Steam API settings dependency.

    Returns:
        SteamStatsResponse: Steam stats including total games and playtime.

    Raises:
        HTTPException: For Steam API errors or invalid responses.
    """
    try:
        return await get_steam_stats(client, settings)

    except TimeoutException:
        msg = "Steam API request timed out"
        raise HTTPException(status_code=504, detail=msg) from None

    except HTTPStatusError as e:
        msg = f"Steam API returned status {e.response.status_code}"
        raise HTTPException(status_code=502, detail=msg) from e

    except RequestError as e:
        msg = "Failed to reach Steam API"
        raise HTTPException(status_code=502, detail=msg) from e

    except TypeError as e:
        msg = f"Invalid Steam API response: {e}"
        raise HTTPException(status_code=502, detail=msg) from e
