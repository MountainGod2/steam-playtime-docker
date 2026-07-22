"""Schema models for Steam API payloads and API responses."""

from pydantic import BaseModel, ConfigDict, Field


class SteamBaseModel(BaseModel):
    """Shared base model for Steam API payloads."""

    model_config = ConfigDict(extra="ignore")


class SteamGame(SteamBaseModel):
    """Relevant fields from a Steam-owned game."""

    playtime_forever: int = Field(default=0, ge=0)


class SteamOwnedGamesData(SteamBaseModel):
    """Owned-games payload nested under the Steam response."""

    games: list[SteamGame]


class SteamOwnedGamesResponse(SteamBaseModel):
    """Response returned by Steam's GetOwnedGames endpoint."""

    response: SteamOwnedGamesData


class SteamStatsResponse(BaseModel):
    """Response model for Steam statistics."""

    total_games: int
    total_playtime_forever_minutes: int
    total_playtime_forever_hours: float
