FROM ghcr.io/astral-sh/uv:bookworm-slim@sha256:85c530098e4db6143cf1b63d1634a9150210a3f98690b3eb6e9fa6515bc60954 AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_NO_DEV=1

ENV UV_PYTHON_INSTALL_DIR=/python

ENV UV_PYTHON_PREFERENCE=only-managed

RUN uv python install 3.12

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM debian:bookworm-slim@sha256:56ff6d36d4eb3db13a741b342ec466f121480b5edded42e4b7ee850ce7a418ee

RUN groupadd --system --gid 999 nonroot \
 && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=python:python /python /python

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

EXPOSE 3000

CMD ["uvicorn", "steam_playtime_docker.main:app", "--host", "0.0.0.0", "--port", "3000", "--log-level", "error"]