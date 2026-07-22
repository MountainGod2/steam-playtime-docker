"""Steam specific endpoints."""

from fastapi import APIRouter

from app.dependencies import ClientDependency, SettingsDependency
from app.schemas.steam import SteamStatsResponse
from app.services.steam import get_steam_stats

router = APIRouter()


@router.get("/steam-stats")
async def steam_stats(client: ClientDependency, settings: SettingsDependency) -> SteamStatsResponse:
    """API endpoint to return Steam stats.

    Args:
        client: The injected aiohttp client session dependency.
        settings: The injected Steam API settings dependency.

    Returns:
        SteamStatsResponse: Steam stats including total games and playtime.

    """
    return await get_steam_stats(client, settings)
