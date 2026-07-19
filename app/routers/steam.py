"""Steam specific endpoints."""

import aiohttp
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.dependencies import ClientDependency, Settings, SettingsDependency


class InvalidSteamResponseError(Exception):
    """Custom exception for invalid Steam API responses."""


router = APIRouter()

STEAM_OWNED_GAMES_URL = (
    "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
)


class SteamGame(BaseModel):
    """Relevant fields from a Steam-owned game."""

    model_config = ConfigDict(extra="ignore")

    playtime_forever: int = Field(default=0, ge=0)


class SteamOwnedGamesData(BaseModel):
    """Owned-games payload nested under the Steam response."""

    model_config = ConfigDict(extra="ignore")

    games: list[SteamGame] = Field(default_factory=list)


class SteamOwnedGamesResponse(BaseModel):
    """Response returned by Steam's GetOwnedGames endpoint."""

    model_config = ConfigDict(extra="ignore")

    response: SteamOwnedGamesData


class SteamStatsResponse(BaseModel):
    """Response model for Steam statistics."""

    total_games: int
    total_playtime_forever_minutes: int
    total_playtime_forever_hours: float


async def get_steam_stats(
    client: aiohttp.ClientSession, settings: Settings
) -> SteamStatsResponse:
    """Fetch Steam-owned games and calculate total playtime.

    Args:
        client: The aiohttp client session to use.
        settings: The Steam API settings containing user and key.

    Returns:
        SteamStatsResponse: Total games and total playtime in minutes and hours.

    Raises:
        InvalidSteamResponseError: If the Steam API response is invalid.
    """
    params = {
        "key": settings.api_key,
        "steamid": settings.user_id,
        "format": "json",
        "include_appinfo": 1,
    }

    async with client.get(STEAM_OWNED_GAMES_URL, params=params) as response:
        try:
            payload = SteamOwnedGamesResponse.model_validate(
                await response.json()
            )
        except ValidationError as exc:
            msg = "Steam API returned an invalid response"
            raise InvalidSteamResponseError(msg) from exc

        total_playtime_minutes = sum(
            game.playtime_forever for game in payload.response.games
        )

    return SteamStatsResponse(
        total_games=len(payload.response.games),
        total_playtime_forever_minutes=total_playtime_minutes,
        total_playtime_forever_hours=round(total_playtime_minutes / 60, 1),
    )


@router.get("/steam-stats")
async def steam_stats(
    client: ClientDependency, settings: SettingsDependency
) -> SteamStatsResponse:
    """API endpoint to return Steam stats.

    Args:
        client: The injected aiohttp client session dependency.
        settings: The injected Steam API settings dependency.

    Returns:
        SteamStatsResponse: Steam stats including total games and playtime.

    Raises:
        HTTPException: For Steam API errors or invalid responses.
    """
    try:
        return await get_steam_stats(client, settings)

    except TimeoutError:
        msg = "Steam API request timed out"
        raise HTTPException(status_code=504, detail=msg) from None

    except aiohttp.ClientResponseError as e:
        msg = f"Steam API returned status {e.status}"
        raise HTTPException(status_code=502, detail=msg) from e

    except aiohttp.ClientError as e:
        msg = "Failed to reach Steam API"
        raise HTTPException(status_code=502, detail=msg) from e

    except TypeError as e:
        msg = f"Invalid Steam API response: {e}"
        raise HTTPException(status_code=502, detail=msg) from e
