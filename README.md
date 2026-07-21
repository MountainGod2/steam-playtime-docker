# Steam Playtime API

FastAPI service that wraps the Steam Web API and returns aggregate playtime stats as JSON.

## Configuration

```bash
cp .env.example .env
```

Set:

- `STEAM_API_KEY` — Steam Web API key
- `STEAM_ID_64` — SteamID64 to query
- `ROOT_PATH` — optional, set only if running behind a reverse proxy at a sub-path (e.g. `/proxy/8000/`)

## Run

```bash
docker run \
  --rm \
  -p 8000:3000 \
  --env-file .env \
  ghcr.io/mountaingod2/steam-playtime-docker:latest
```

## Endpoints

- `GET /health` — liveness check
- `GET /steam-stats` — total games + total playtime
- `GET /docs` — Swagger UI
- `GET /redoc` — ReDoc

`GET /steam-stats` response:

```json
{
  "total_games": 125,
  "total_playtime_forever_minutes": 42000,
  "total_playtime_forever_hours": 700.0
}
```

Timeouts from Steam return `504`. Connection errors, bad upstream status codes, or malformed responses return `502`.
