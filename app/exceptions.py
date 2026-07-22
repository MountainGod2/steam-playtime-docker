"""Application-specific exception types."""

from dataclasses import dataclass


@dataclass(slots=True)
class AppHTTPError(Exception):
    """Domain-level error that maps directly to an HTTP response."""

    status_code: int
    detail: str
