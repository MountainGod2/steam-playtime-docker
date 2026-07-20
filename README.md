# Steam Playtime API

FastAPI service that aggregates total playtime from the Steam Web API.

## Configuration

Copy the example file and set the required values:

```bash
cp .env.example .env
```

- `STEAM_API_KEY`: Steam Web API key.
- `STEAM_ID_64`: SteamID64 of the account to query.
- `ROOT_PATH`: Optional external path prefix when serving behind a reverse
  proxy, such as `/proxy/8000/`.

The queried Steam profile must expose its game details for Steam to return the
owned-games data.

## Run

```bash
docker run \
  --rm \
  -p 8000:3000 \
  --env-file .env \
  ghcr.io/mountaingod2/steam-playtime-docker:latest
```

## Endpoints

- `GET /health`: Process liveness check.
- `GET /steam-stats`: Total owned games and lifetime playtime.
- `GET /docs`: Interactive Swagger UI.
- `GET /redoc`: ReDoc API documentation.

Example response from `GET /steam-stats`:

```json
{
  "total_games": 125,
  "total_playtime_forever_minutes": 42000,
  "total_playtime_forever_hours": 700.0
}
```

Steam request timeouts return HTTP `504`. Upstream connection, HTTP, and
response-validation failures return HTTP `502`.
