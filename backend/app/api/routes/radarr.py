# ============================================================================
# MicroManagerr - Radarr Integration Endpoints
# ============================================================================
# This module handles all API endpoints related to Radarr.
#
# WHAT IS RADARR?
# Radarr is a movie collection manager. It:
# - Monitors for movie releases
# - Downloads them automatically
# - Organizes your movie library
# - Manages quality upgrades
#
# RADARR API BASICS:
# - Base URL: http://your-server:7878/api/v3
# - Authentication: X-Api-Key header
# - Format: JSON
# - Docs: https://radarr.video/docs/api/
#
# NOTE: Radarr's API is very similar to Sonarr's (they share a codebase).
# The main differences:
# - "movie" instead of "series"
# - Movies don't have seasons/episodes
# - Different metadata fields
# ============================================================================

import logging
from typing import List, Optional

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

class RadarrConnectionRequest(BaseModel):
    """Request body for testing Radarr connection."""

    url: str = Field(
        ...,
        description="Radarr base URL (e.g., http://localhost:7878)",
        examples=["http://localhost:7878", "http://radarr:7878"]
    )
    api_key: str = Field(
        ...,
        description="Radarr API key (found in Settings -> General)",
        min_length=32,
        max_length=32
    )


class RadarrStatusResponse(BaseModel):
    """Response for Radarr status check."""

    connected: bool
    version: Optional[str] = None
    url: Optional[str] = None
    error: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "connected": True,
                "version": "5.3.6.8612",
                "url": "http://localhost:7878",
                "error": None
            }
        }
    }


class RadarrMovieResponse(BaseModel):
    """Simplified movie information from Radarr."""

    id: int
    title: str
    year: int
    path: str
    monitored: bool
    tags: List[int]
    quality_profile_id: int
    has_file: bool
    runtime: int  # Runtime in minutes - useful for edition detection!

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "The Matrix",
                "year": 1999,
                "path": "/movies/The Matrix (1999)",
                "monitored": True,
                "tags": [1, 3],
                "quality_profile_id": 4,
                "has_file": True,
                "runtime": 136
            }
        }
    }


class RadarrTagResponse(BaseModel):
    """Tag information from Radarr."""

    id: int
    label: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "label": "Dolby-Vision"
            }
        }
    }


class RadarrTagCreateRequest(BaseModel):
    """Request to create a new tag in Radarr."""

    label: str = Field(
        ...,
        description="The tag label to create",
        min_length=1,
        max_length=50,
        examples=["HDR", "Dolby-Vision", "IMAX"]
    )


# =============================================================================
# Dependency Helpers
# =============================================================================

def require_radarr_configured() -> None:
    """
    Raise an exception if Radarr is not configured.

    Raises:
        HTTPException: 503 if Radarr is not configured
    """
    if not settings.radarr_configured:
        logger.warning("Radarr endpoint called but Radarr is not configured")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": "Radarr not configured",
                "message": "Please set RADARR_URL and RADARR_API_KEY environment variables",
                "docs": "See /docs for configuration instructions"
            }
        )


# =============================================================================
# API Endpoints
# =============================================================================

@router.get(
    "/status",
    response_model=RadarrStatusResponse,
    summary="Get Radarr connection status",
    description="Check if Radarr is configured and reachable.",
)
async def get_radarr_status() -> RadarrStatusResponse:
    """
    Get current Radarr connection status.

    Returns:
        RadarrStatusResponse: Connection status and version if connected
    """
    if not settings.radarr_configured:
        return RadarrStatusResponse(
            connected=False,
            error="Radarr not configured. Set RADARR_URL and RADARR_API_KEY."
        )

    # TODO: Phase 3 - Actually call Radarr API
    return RadarrStatusResponse(
        connected=True,
        version="(pending implementation)",
        url=settings.radarr_url,
    )


@router.post(
    "/test-connection",
    response_model=RadarrStatusResponse,
    summary="Test Radarr connection with provided credentials",
    description="Test connection to Radarr with user-provided URL and API key.",
)
async def test_radarr_connection(
    connection: RadarrConnectionRequest
) -> RadarrStatusResponse:
    """
    Test connection to Radarr with provided credentials.

    Args:
        connection: URL and API key to test

    Returns:
        RadarrStatusResponse: Whether connection succeeded
    """
    # TODO: Phase 3 - Implement actual connection test
    logger.info(f"Test connection requested for: {connection.url}")
    return RadarrStatusResponse(
        connected=True,
        version="(pending implementation)",
        url=connection.url,
    )


@router.get(
    "/movies",
    response_model=List[RadarrMovieResponse],
    summary="Get all movies from Radarr",
    description="Fetch all movies from your Radarr library.",
)
async def get_all_movies() -> List[RadarrMovieResponse]:
    """
    Get all movies from Radarr.

    This endpoint fetches your complete movie library from Radarr.
    It's used to:
    1. Display your library in MicroManagerr
    2. Show what content can be scanned for HDR/DV
    3. Select movies for tag application
    4. Compare runtimes for edition detection

    Returns:
        List[RadarrMovieResponse]: All movies in Radarr

    Raises:
        HTTPException: 503 if Radarr is not configured
    """
    require_radarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # The response from Radarr looks like:
    # [
    #     {
    #         "id": 1,
    #         "title": "The Matrix",
    #         "year": 1999,
    #         "path": "/movies/The Matrix (1999)",
    #         "monitored": true,
    #         "hasFile": true,
    #         "runtime": 136,
    #         "qualityProfileId": 4,
    #         "tags": [1, 2],
    #         "movieFile": {  // Only present if hasFile is true
    #             "path": "/movies/The Matrix (1999)/The.Matrix.1999.2160p.UHD.BluRay.x265-EXAMPLE.mkv",
    #             "size": 45678901234,
    #             "quality": {...}
    #         }
    #     },
    #     ...
    # ]

    logger.info("Fetching all movies from Radarr")
    return []


@router.get(
    "/movies/{movie_id}",
    response_model=RadarrMovieResponse,
    summary="Get a specific movie from Radarr",
    description="Fetch details for a single movie by ID.",
)
async def get_movie(movie_id: int) -> RadarrMovieResponse:
    """
    Get a specific movie from Radarr.

    This is useful for:
    1. Getting updated info after modifications
    2. Checking current tag state
    3. Getting file path for scanning

    Args:
        movie_id: Radarr's internal movie ID

    Returns:
        RadarrMovieResponse: Movie details

    Raises:
        HTTPException: 503 if Radarr not configured
        HTTPException: 404 if movie not found
    """
    require_radarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # GET /api/v3/movie/{id}

    logger.info(f"Fetching movie {movie_id} from Radarr")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id} not found (endpoint pending implementation)"
    )


@router.get(
    "/tags",
    response_model=List[RadarrTagResponse],
    summary="Get all tags from Radarr",
    description="Fetch all available tags from Radarr.",
)
async def get_all_tags() -> List[RadarrTagResponse]:
    """
    Get all tags from Radarr.

    Tags in Radarr work exactly like Sonarr tags.
    MicroManagerr uses them to mark content with detected features.

    Common tags we might create:
    - HDR
    - HDR10+
    - Dolby-Vision
    - DV-Profile-5
    - DV-Profile-8
    - IMAX
    - Extended-Edition
    - Directors-Cut

    Returns:
        List[RadarrTagResponse]: All tags in Radarr
    """
    require_radarr_configured()

    # TODO: Phase 3 - Implement actual API call
    logger.info("Fetching all tags from Radarr")
    return []


@router.post(
    "/tags",
    response_model=RadarrTagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tag in Radarr",
    description="Create a new tag that can be applied to movies.",
)
async def create_tag(tag: RadarrTagCreateRequest) -> RadarrTagResponse:
    """
    Create a new tag in Radarr.

    MicroManagerr will use this to create tags like:
    - "HDR" for HDR10 content
    - "Dolby-Vision" for DV content
    - "IMAX" for IMAX Enhanced content

    Args:
        tag: The tag to create

    Returns:
        RadarrTagResponse: The created tag with its assigned ID

    Raises:
        HTTPException: 400 if tag already exists
        HTTPException: 503 if Radarr not configured
    """
    require_radarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # POST /api/v3/tag
    # Body: {"label": "HDR"}
    # Returns: {"id": 5, "label": "HDR"}

    logger.info(f"Creating tag in Radarr: {tag.label}")

    # Placeholder response
    return RadarrTagResponse(
        id=999,  # Placeholder
        label=tag.label
    )


@router.put(
    "/movies/{movie_id}/tags",
    response_model=RadarrMovieResponse,
    summary="Update tags on a movie",
    description="Set the tags for a specific movie.",
)
async def update_movie_tags(
    movie_id: int,
    tag_ids: List[int]
) -> RadarrMovieResponse:
    """
    Update the tags on a movie.

    This is the core operation for MicroManagerr - after detecting
    that a movie has HDR/DV/IMAX, we apply the appropriate tags.

    How it works:
    1. Fetch the current movie data
    2. Update the tags array
    3. PUT the entire movie object back

    Args:
        movie_id: Radarr's internal movie ID
        tag_ids: List of tag IDs to apply

    Returns:
        RadarrMovieResponse: Updated movie with new tags

    Raises:
        HTTPException: 404 if movie not found
        HTTPException: 503 if Radarr not configured

    Example:
        # Add HDR (id=1) and DV (id=2) tags to movie 42
        PUT /api/v1/radarr/movies/42/tags
        Body: [1, 2]
    """
    require_radarr_configured()

    # TODO: Phase 3 - Implement actual API call
    # The Radarr API requires PUTting the entire movie object
    # So we need to:
    # 1. GET /api/v3/movie/{id} to get current data
    # 2. Modify movie["tags"] = tag_ids
    # 3. PUT /api/v3/movie/{id} with the modified object
    #
    # This is a common pattern in REST APIs - you fetch, modify, and PUT back

    logger.info(f"Updating tags on movie {movie_id}: {tag_ids}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Movie {movie_id} not found (endpoint pending implementation)"
    )


# =============================================================================
# LEARNING NOTE: REST API Design Patterns
# =============================================================================
# The Sonarr/Radarr APIs follow REST conventions:
#
# Resource-Based URLs:
#   /api/v3/movie          - Collection of movies
#   /api/v3/movie/42       - Single movie with ID 42
#   /api/v3/movie/42/file  - File related to movie 42
#
# HTTP Methods:
#   GET    - Read data (safe, no side effects)
#   POST   - Create new resources
#   PUT    - Update entire resources
#   PATCH  - Update partial resources (not commonly used in Arr APIs)
#   DELETE - Remove resources
#
# Status Codes:
#   200 - Success
#   201 - Created (successful POST)
#   400 - Bad request (client error)
#   404 - Not found
#   500 - Server error
#
# When designing MicroManagerr's API, we follow these same patterns
# so developers familiar with REST feel at home.
# =============================================================================
