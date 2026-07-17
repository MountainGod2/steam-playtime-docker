"""Health check endpoint."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Response model for health checks."""

    status: str


@router.get("/health")
async def health() -> HealthResponse:
    """API endpoint for container/orchestrator health checks.

    Returns:
        HealthResponse: Static status indicating the app is running and
            able to serve requests.
    """
    return HealthResponse(status="ok")
