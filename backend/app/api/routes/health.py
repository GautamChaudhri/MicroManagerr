# ============================================================================
# MicroManagerr - Health Check Endpoints
# ============================================================================
# Health checks are essential for:
# 1. Monitoring - Is the service alive?
# 2. Container orchestration - Docker/Kubernetes use these to restart unhealthy containers
# 3. Load balancers - Route traffic only to healthy instances
# 4. Debugging - Quick way to verify the service is responding
#
# BEST PRACTICES:
# - Keep health checks fast (no complex operations)
# - Return structured data (easy for monitoring tools)
# - Include dependency status (database, external services)
# - Use appropriate HTTP status codes (200 OK, 503 Service Unavailable)
# ============================================================================

from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter, status
from pydantic import BaseModel

from app import __version__
from app.config import settings

# =============================================================================
# Router Setup
# =============================================================================
# APIRouter is like a mini-FastAPI app. It groups related endpoints together.
# Later, we add it to the main app with app.include_router(router)
# =============================================================================

router = APIRouter()


# =============================================================================
# Response Schemas
# =============================================================================
# Pydantic models define the shape of API responses.
# FastAPI uses these to:
# 1. Generate documentation
# 2. Validate response data
# 3. Serialize data to JSON
#
# WHY DEFINE RESPONSE MODELS?
# - Clear API contract (developers know what to expect)
# - Auto-generated docs are accurate
# - Catches bugs if response shape is wrong
# =============================================================================

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str
    timestamp: str
    version: str

    # Pydantic v2 configuration
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T12:00:00Z",
                "version": "0.1.0"
            }
        }
    }


class DetailedHealthResponse(BaseModel):
    """Response model for detailed health check."""

    status: str
    timestamp: str
    version: str
    services: Dict[str, Any]
    config: Dict[str, Any]

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-15T12:00:00Z",
                "version": "0.1.0",
                "services": {
                    "database": {"status": "connected"},
                    "sonarr": {"status": "configured", "url": "http://localhost:8989"},
                    "radarr": {"status": "not_configured"}
                },
                "config": {
                    "debug": False,
                    "log_level": "INFO"
                }
            }
        }
    }


# =============================================================================
# Health Check Endpoints
# =============================================================================

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
    description="Returns basic health status. Use this for simple liveness checks.",
)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint.

    This is a simple "is the service alive?" check.
    It doesn't verify dependencies - just that the API is responding.

    Returns:
        HealthResponse: Basic health information

    HTTP Status Codes:
        - 200: Service is healthy and responding
        - 5xx: Service is down (this would be returned by the infrastructure, not this code)
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=__version__,
    )


@router.get(
    "/health/detailed",
    response_model=DetailedHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed health check",
    description="Returns detailed health status including dependency states.",
)
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed health check endpoint.

    This checks all dependencies and provides comprehensive status information.
    Use this for debugging or detailed monitoring.

    What it checks:
    - Database connection status
    - Sonarr/Radarr configuration and connectivity
    - Application configuration

    Returns:
        DetailedHealthResponse: Comprehensive health information

    Note:
        This endpoint does more work than the basic health check.
        For high-frequency monitoring, prefer /health.
    """
    # Build services status
    services = {
        "database": {
            "status": "not_implemented",  # TODO: Add actual DB check in Phase 1
            "note": "Database health check will be added in Phase 1"
        },
        "sonarr": {
            "status": "configured" if settings.sonarr_configured else "not_configured",
            "url": settings.sonarr_url if settings.sonarr_configured else None,
            # TODO: Add actual connectivity check
        },
        "radarr": {
            "status": "configured" if settings.radarr_configured else "not_configured",
            "url": settings.radarr_url if settings.radarr_configured else None,
            # TODO: Add actual connectivity check
        },
    }

    # Determine overall status
    # For now, we're always "healthy" since we haven't implemented real checks
    # In the future, this should reflect actual dependency status
    overall_status = "healthy"

    return DetailedHealthResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=__version__,
        services=services,
        config={
            "debug": settings.debug,
            "log_level": settings.log_level,
        },
    )


# =============================================================================
# LEARNING NOTE: HTTP Status Codes
# =============================================================================
# Status codes tell clients whether a request succeeded and why it failed.
#
# 2xx - Success:
#   200 OK - Request succeeded
#   201 Created - Resource was created
#   204 No Content - Success, but nothing to return
#
# 4xx - Client Error (caller's fault):
#   400 Bad Request - Invalid request format
#   401 Unauthorized - Not authenticated
#   403 Forbidden - Authenticated but not allowed
#   404 Not Found - Resource doesn't exist
#   422 Unprocessable Entity - Validation failed (FastAPI uses this)
#
# 5xx - Server Error (our fault):
#   500 Internal Server Error - Something broke
#   502 Bad Gateway - Upstream service failed
#   503 Service Unavailable - Service is down/overloaded
# =============================================================================
