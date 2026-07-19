import re

from aioresponses import aioresponses
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_steam_stats_returns_aggregated_totals(client: TestClient) -> None:
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
        mocked.get(
            re.compile(
                r"https://api\.steampowered\.com/.*/GetOwnedGames/v0001/.*"
            ),
            payload=payload,
            status=200,
        )

        response = client.get("/steam-stats")

    assert response.status_code == 200
    assert response.json() == {
        "total_games": 3,
        "total_playtime_forever_minutes": 150,
        "total_playtime_forever_hours": 2.5,
    }


def test_steam_stats_returns_502_for_invalid_payload(
    client: TestClient,
) -> None:
    payload = {"unexpected": {}}

    with aioresponses() as mocked:
        mocked.get(
            re.compile(
                r"https://api\.steampowered\.com/.*/GetOwnedGames/v0001/.*"
            ),
            payload=payload,
            status=200,
        )

        response = client.get("/steam-stats")

    assert response.status_code == 502
    assert "Invalid Steam API response" in response.json()["detail"]
