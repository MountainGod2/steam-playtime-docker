"""Application-wide exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .exceptions import AppHTTPError


def handle_app_http_error(_request: Request, exc: Exception) -> JSONResponse:
    """Convert domain-level HTTP errors to JSON API responses.

    Returns:
        JSONResponse: A JSON payload with a status code and error detail.
    """
    if not isinstance(exc, AppHTTPError):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register app-level exception handlers."""
    app.add_exception_handler(AppHTTPError, handle_app_http_error)
