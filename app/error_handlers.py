"""Application-wide exception handlers."""

import logging
from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import AppHTTPError

logger = logging.getLogger(__name__)


def handle_app_http_error(_request: Request, exc: Exception) -> JSONResponse:
    """Convert domain-level HTTP errors to JSON API responses.

    Returns:
        JSONResponse: A JSON payload with a status code and error detail.
    """
    app_http_error = cast("AppHTTPError", exc)
    return JSONResponse(
        status_code=app_http_error.status_code,
        content={"detail": app_http_error.detail},
    )


def handle_unexpected_exception(_request: Request, exc: Exception) -> JSONResponse:
    """Convert uncaught server errors to a consistent JSON response.

    Returns:
        JSONResponse: Standardized 500 error payload for unexpected failures.
    """
    logger.error("Unhandled exception while processing request", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register app-level exception handlers."""
    app.add_exception_handler(AppHTTPError, handle_app_http_error)
    app.add_exception_handler(Exception, handle_unexpected_exception)
