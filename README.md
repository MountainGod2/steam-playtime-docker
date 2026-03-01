# Steam Playtime API

FastAPI service that aggregates total playtime from the Steam Web API.

## Configuration

Set the following environment variables:

- `STEAM_API_KEY`
- `STEAM_ID_64`

## Run

```bash
docker run \
  --rm \
  -it \
  -p 8000:3000 \ # HOST:CONTAINER (only adjust host)
  -e STEAM_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" \
  -e STEAM_ID_64="XXXXXXXXXXXXXXXXX" \
  mountaingod2/steam_playtime_docker:dev
```

## Endpoint

- `GET /steam-stats`

Returns total games and playtime in minutes and hours.
