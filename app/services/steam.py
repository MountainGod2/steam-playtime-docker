"""Steam API integration and aggregation logic."""

import aiohttp
from pydantic import ValidationError

from app.config import Settings
from app.exceptions import AppHTTPError
from app.schemas.steam import SteamOwnedGamesResponse, SteamStatsResponse

STEAM_OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"


async def get_steam_stats(client: aiohttp.ClientSession, settings: Settings) -> SteamStatsResponse:
    """Fetch Steam-owned games and calculate total playtime.

    Returns:
        SteamStatsResponse: Aggregated game count and playtime totals.

    Raises:
        AppHTTPError: If the Steam API call fails or returns invalid data.
    """
    params = {
        "key": settings.steam_api_key.get_secret_value(),
        "steamid": settings.steam_id_64,
        "format": "json",
    }

    try:
        async with client.get(STEAM_OWNED_GAMES_URL, params=params) as response:
            response.raise_for_status()
            payload = SteamOwnedGamesResponse.model_validate(await response.json())
    except TimeoutError as exc:
        raise AppHTTPError(504, "Steam API request timed out") from exc
    except aiohttp.ClientResponseError as exc:
        msg = f"Steam API returned status {exc.status}"
        raise AppHTTPError(502, msg) from exc
    except aiohttp.ClientError as exc:
        raise AppHTTPError(502, "Failed to reach Steam API") from exc
    except (aiohttp.ContentTypeError, ValidationError, ValueError) as exc:
        msg = "Steam API returned an invalid response"
        raise AppHTTPError(502, msg) from exc

    total_playtime_minutes = sum(game.playtime_forever for game in payload.response.games)
    return SteamStatsResponse(
        total_games=len(payload.response.games),
        total_playtime_forever_minutes=total_playtime_minutes,
        total_playtime_forever_hours=round(total_playtime_minutes / 60, 1),
    )
