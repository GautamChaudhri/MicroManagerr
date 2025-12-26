# ============================================================================
# MicroManagerr - Sonarr Integration Endpoints
# ============================================================================
# This module handles all API endpoints related to Sonarr.
#
# WHAT IS SONARR?
# Sonarr is a PVR (Personal Video Recorder) for TV shows. It:
# - Monitors for new episodes
# - Downloads them automatically
# - Organizes your library
# - Manages quality upgrades
#
# SONARR API BASICS:
# - Base URL: http://your-server:8989/api/v3
# - Authentication: X-Api-Key header
# - Format: JSON
# - Docs: https://sonarr.tv/docs/api/
#
# We'll wrap Sonarr's API with our own endpoints to:
# 1. Abstract away Sonarr-specific details
# 2. Add our own logic (HDR detection, tagging)
# 3. Provide a unified interface across Sonarr/Radarr
# ============================================================================

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.config import settings

# Set up logging for this module
logger = logging.getLogger(__name__)

# Create the router
router = APIRouter()


# =============================================================================
# Pydantic Schemas
# =============================================================================
# These define the structure of data coming in and going out of our API.
#
# REQUEST SCHEMAS: What the client sends to us
# RESPONSE SCHEMAS: What we send back to the client
#
# The naming convention used:
# - XxxRequest: Input data for POST/PUT requests
# - XxxResponse: Output data structure
# - XxxBase: Shared fields between Request/Response
# =============================================================================

class SonarrConnectionRequest(BaseModel):
    """Request body for testing Sonarr connection."""

    url: str = Field(
        ...,  # ... means required
        description="Sonarr base URL (e.g., http://localhost:8989)",
        examples=["http://localhost:8989", "http://sonarr:8989"]
    )
    api_key: str = Field(
        ...,
        description="Sonarr API key (found in Settings -> General)",
        min_length=32,
        max_length=32
    )


class SonarrStatusResponse(BaseModel):
    """Response for Sonarr status check."""

    connected: bool
    version: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "connected": True,
                "version": "4.0.0.748",
                "url": "http://localhost:8989",
                "error": None
            }
        }
    }


class SonarrSeriesResponse(BaseModel):
    """Simplified series information from Sonarr."""

    id: int
    title: str
    year: int
    path: str
    monitored: bool
    tags: List[int]
    quality_profile_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Breaking Bad",
                "year": 2008,
                "path": "/tv/Breaking Bad",
                "monitored": True,
                "tags": [1, 2],
                "quality_profile_id": 4
            }
        }
    }


class SonarrTagResponse(BaseModel):
    """Tag information from Sonarr."""

    id: int
    label: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "label": "HDR"
            }
        }
    }


# =============================================================================
# Dependency Helpers
# =============================================================================
# These functions are reused across endpoints.
# They handle common operations like validating configuration.
# =============================================================================

def require_sonarr_configured() -> None:
    """
    Raise an exception if Sonarr is not configured.

    This is a guard function - call it at the start of any endpoint
    that requires Sonarr to be set up.

    Raises:
        HTTPException: 503 if Sonarr is not configured
    """
    if not settings.sonarr_configured:
        logger.warning("Sonarr endpoint called but Sonarr is not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Sonarr not configured",
                "message": "Please set SONARR_URL and SONARR_API_KEY environment variables",
                "docs": "See /docs for configuration instructions"
            }
        )


# =============================================================================
# API Endpoints
# =============================================================================

@router.get(
    "/status",
    response_model=SonarrStatusResponse,
    summary="Get Sonarr connection status",
    description="Check if Sonarr is configured and reachable.",
)
async def get_sonarr_status() -> SonarrStatusResponse:
    """
    Get current Sonarr connection status.

    This endpoint checks:
    1. Is Sonarr configured? (URL and API key set)
    2. Can we reach Sonarr? (makes test API call)

    Returns:
        SonarrStatusResponse: Connection status and version if connected

    Note:
        This is a good endpoint to call on frontend page load
        to show Sonarr connection status in the UI.
    """
    if not settings.sonarr_configured:
        return SonarrStatusResponse(
            connected=False,
            error="Sonarr not configured. Set SONARR_URL and SONARR_API_KEY."
        )

    # TODO: Phase 3 - Actually call Sonarr API to verify connection
    # For now, we just report that it's configured
    #
    # The actual implementation will look like:
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{settings.sonarr_url}/api/v3/system/status",
    #         headers={"X-Api-Key": settings.sonarr_api_key}
    #     )
    #     data = response.json()
    #     return SonarrStatusResponse(
    #         connected=True,
    #         version=data["version"],
    #         url=settings.sonarr_url
    #     )

    return SonarrStatusResponse(
        connected=True,  # Placeholder - will be actual check later
        version="(pending implementation)",
        url=settings.sonarr_url,
    )


@router.post(
    "/test-connection",
    response_model=SonarrStatusResponse,
    summary="Test Sonarr connection with provided credentials",
    description="Test connection to Sonarr with user-provided URL and API key.",
)
async def test_sonarr_connection(
    connection: SonarrConnectionRequest
) -> SonarrStatusResponse:
    """
    Test connection to Sonarr with provided credentials.

    This is useful for:
    1. First-time setup (before saving config)
    2. Verifying credentials are correct
    3. UI "Test Connection" button

    Args:
        connection: URL and API key to test

    Returns:
        SonarrStatusResponse: Whether connection succeeded

    Note:
        This does NOT save the credentials. It only tests them.
        Use a separate endpoint to persist credentials.
    """
    # TODO: Phase 3 - Implement actual connection test
    # async with httpx.AsyncClient() as client:
    #     try:
    #         response = await client.get(
    #             f"{connection.url}/api/v3/system/status",
    #             headers={"X-Api-Key": connection.api_key},
    #             timeout=10.0  # Don't hang forever
    #         )
    #         response.raise_for_status()
    #         data = response.json()
    #         return SonarrStatusResponse(
    #             connected=True,
    #             version=data["version"],
    #             url=connection.url
    #         )
    #     except httpx.HTTPError as e:
    #         return SonarrStatusResponse(
    #             connected=False,
    #             error=f"Connection failed: {str(e)}"
    #         )

    # Placeholder response
    logger.info(f"Test connection requested for: {connection.url}")
    return SonarrStatusResponse(
        connected=True,
        version="(pending implementation)",
        url=connection.url,
    )


@router.get(
    "/series",
    response_model=List[SonarrSeriesResponse],
    summary="Get all series from Sonarr",
    description="Fetch all TV series from your Sonarr library.",
)
async def get_all_series() -> List[SonarrSeriesResponse]:
    """
    Get all series from Sonarr.

    This endpoint fetches your complete TV library from Sonarr.
    It's used to:
    1. Display your library in MicroManagerr
    2. Show what content can be scanned for HDR
    3. Select series for tag application

    Returns:
        List[SonarrSeriesResponse]: All series in Sonarr

    Raises:
        HTTPException: 503 if Sonarr is not configured
    """
    require_sonarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{settings.sonarr_url}/api/v3/series",
    #         headers={"X-Api-Key": settings.sonarr_api_key}
    #     )
    #     series_list = response.json()
    #     return [
    #         SonarrSeriesResponse(
    #             id=s["id"],
    #             title=s["title"],
    #             year=s.get("year", 0),
    #             path=s["path"],
    #             monitored=s["monitored"],
    #             tags=s.get("tags", []),
    #             quality_profile_id=s["qualityProfileId"]
    #         )
    #         for s in series_list
    #     ]

    # Placeholder - return empty list for now
    logger.info("Fetching all series from Sonarr")
    return []


@router.get(
    "/tags",
    response_model=List[SonarrTagResponse],
    summary="Get all tags from Sonarr",
    description="Fetch all available tags from Sonarr.",
)
async def get_all_tags() -> List[SonarrTagResponse]:
    """
    Get all tags from Sonarr.

    Tags in Sonarr are used to categorize and filter content.
    MicroManagerr will:
    1. List existing tags (like "HDR", "4K")
    2. Create new tags if needed
    3. Apply tags to detected content

    Returns:
        List[SonarrTagResponse]: All tags in Sonarr

    Raises:
        HTTPException: 503 if Sonarr is not configured
    """
    require_sonarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{settings.sonarr_url}/api/v3/tag",
    #         headers={"X-Api-Key": settings.sonarr_api_key}
    #     )
    #     tags = response.json()
    #     return [
    #         SonarrTagResponse(id=t["id"], label=t["label"])
    #         for t in tags
    #     ]

    logger.info("Fetching all tags from Sonarr")
    return []


# =============================================================================
# LEARNING NOTE: FastAPI Dependency Injection
# =============================================================================
# In larger applications, you'll use FastAPI's dependency injection system.
# Instead of calling require_sonarr_configured() at the start of each endpoint,
# you can use Depends():
#
# from fastapi import Depends
#
# async def get_sonarr_client() -> SonarrClient:
#     """Dependency that provides a configured Sonarr client."""
#     if not settings.sonarr_configured:
#         raise HTTPException(status_code=503, detail="Sonarr not configured")
#     return SonarrClient(settings.sonarr_url, settings.sonarr_api_key)
#
# @router.get("/series")
# async def get_all_series(
#     client: SonarrClient = Depends(get_sonarr_client)
# ) -> List[SonarrSeriesResponse]:
#     return await client.get_all_series()
#
# This pattern:
# 1. Reduces code duplication
# 2. Makes testing easier (you can inject mock clients)
# 3. Handles cleanup automatically
# =============================================================================
