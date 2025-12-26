# ============================================================================
# MicroManagerr - Main Application Entry Point
# ============================================================================
# This is the heart of your FastAPI application!
#
# WHAT THIS FILE DOES:
# 1. Creates the FastAPI application instance
# 2. Configures middleware (request/response processing)
# 3. Registers all API routes
# 4. Sets up startup/shutdown events
#
# HOW TO RUN:
# Development: uvicorn app.main:app --reload
# Production:  uvicorn app.main:app --host 0.0.0.0 --port 8000
#
# The "--reload" flag watches for file changes and restarts automatically.
# Never use --reload in production!
# ============================================================================

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.routes import health, sonarr, radarr
from app.config import settings

# =============================================================================
# Logging Setup
# =============================================================================
# Logging is how your application tells you what's happening.
# During development, you'll want DEBUG level to see everything.
# In production, INFO or WARNING to reduce noise.
#
# Log levels (from most to least verbose):
# - DEBUG: Detailed information, typically only useful when diagnosing problems
# - INFO: Confirmation that things are working as expected
# - WARNING: Something unexpected happened, but the app still works
# - ERROR: A more serious problem, the app couldn't perform some function
# - CRITICAL: A very serious error, the app may not be able to continue
# =============================================================================

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# =============================================================================
# Application Lifespan
# =============================================================================
# The lifespan context manager handles startup and shutdown events.
#
# WHAT HAPPENS HERE:
# - Startup: Initialize database connections, load caches, etc.
# - Shutdown: Close connections gracefully, flush buffers, etc.
#
# WHY USE LIFESPAN?
# - Clean resource management
# - Ensures connections are closed even if the app crashes
# - Required for async setup/teardown
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown.

    Everything before 'yield' runs at startup.
    Everything after 'yield' runs at shutdown.
    """
    # -------------------------------------------------------------------------
    # STARTUP
    # -------------------------------------------------------------------------
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Log level: {settings.log_level}")

    # Log which services are configured
    if settings.sonarr_configured:
        logger.info(f"Sonarr configured at: {settings.sonarr_url}")
    else:
        logger.warning("Sonarr not configured - set SONARR_URL and SONARR_API_KEY")

    if settings.radarr_configured:
        logger.info(f"Radarr configured at: {settings.radarr_url}")
    else:
        logger.warning("Radarr not configured - set RADARR_URL and RADARR_API_KEY")

    # TODO: Initialize database connection (Phase 1)
    # TODO: Initialize background task scheduler (Phase 5)

    yield  # Application runs here

    # -------------------------------------------------------------------------
    # SHUTDOWN
    # -------------------------------------------------------------------------
    logger.info(f"Shutting down {settings.app_name}")

    # TODO: Close database connections
    # TODO: Cancel background tasks


# =============================================================================
# Create FastAPI Application
# =============================================================================
# This is where we create the main FastAPI app instance.
#
# KEY PARAMETERS:
# - title: Shown in the auto-generated docs
# - description: Explains what the API does
# - version: API version (shown in docs)
# - lifespan: Our startup/shutdown handler
# =============================================================================

app = FastAPI(
    title=settings.app_name,
    description="""
    MicroManagerr - Your Media Library Enhancement Tool

    MicroManagerr integrates with Sonarr and Radarr to:
    - Detect HDR, Dolby Vision, and IMAX content
    - Automatically apply tags for better organization
    - Fix letterboxing with MKV crop metadata
    - Find and upgrade to HDR versions of your content
    - Keep your libraries organized and healthy

    ## Getting Started

    1. Configure your Sonarr/Radarr connections
    2. Run a library scan
    3. Review detected content
    4. Apply tags automatically

    ## API Documentation

    - **Interactive docs**: Visit `/docs` for Swagger UI
    - **ReDoc**: Visit `/redoc` for alternative documentation
    """,
    version=__version__,
    lifespan=lifespan,
    # Disable docs in production if needed
    docs_url="/docs" if settings.debug else "/docs",
    redoc_url="/redoc" if settings.debug else "/redoc",
)


# =============================================================================
# Middleware Configuration
# =============================================================================
# Middleware processes every request/response that passes through your API.
# Think of it like a pipeline that requests flow through.
#
# Request -> Middleware 1 -> Middleware 2 -> Your Code -> Middleware 2 -> Middleware 1 -> Response
#
# CORS (Cross-Origin Resource Sharing):
# When your frontend (running on localhost:3000) tries to talk to your API
# (running on localhost:8000), browsers block this by default for security.
# CORS middleware tells browsers "it's okay, I trust these origins."
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    # Origins allowed to make requests
    # In production, you'd list specific domains
    # For development, we allow everything
    allow_origins=["*"] if settings.debug else ["http://localhost:8000"],

    # Allow cookies/authorization headers
    allow_credentials=True,

    # Allow all HTTP methods
    allow_methods=["*"],

    # Allow all headers
    allow_headers=["*"],
)


# =============================================================================
# Register API Routes
# =============================================================================
# Routes are organized into separate files by feature (health, sonarr, etc.)
# We "include" them here to add them to the main app.
#
# WHY ORGANIZE ROUTES THIS WAY?
# 1. Separation of concerns - each file handles one feature
# 2. Easier to find and modify code
# 3. Prevents main.py from becoming huge
# 4. Allows teams to work on different features without conflicts
#
# PREFIX: All routes in the included router start with this prefix
# TAGS: Used to group endpoints in the documentation
# =============================================================================

# Health check endpoints (no prefix - available at root)
app.include_router(
    health.router,
    tags=["Health"],
)

# Sonarr integration endpoints
app.include_router(
    sonarr.router,
    prefix="/api/v1/sonarr",
    tags=["Sonarr"],
)

# Radarr integration endpoints
app.include_router(
    radarr.router,
    prefix="/api/v1/radarr",
    tags=["Radarr"],
)

# TODO: Add more routers as features are built:
# app.include_router(scan.router, prefix="/api/v1/scan", tags=["Scanning"])
# app.include_router(tags.router, prefix="/api/v1/tags", tags=["Tags"])


# =============================================================================
# Root Endpoint
# =============================================================================
# A simple endpoint at the root URL that returns basic API info.
# This is useful for quick "is the API alive?" checks.
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - returns basic API information.

    This is a good place to link to documentation and show API status.
    """
    return {
        "name": settings.app_name,
        "version": __version__,
        "docs": "/docs",
        "health": "/health",
    }


# =============================================================================
# Running the Application
# =============================================================================
# This block runs when you execute: python -m app.main
# However, the preferred way to run FastAPI is with uvicorn:
#   uvicorn app.main:app --reload
#
# The uvicorn command is better because:
# 1. Supports --reload for auto-restart
# 2. Handles worker processes
# 3. Better performance tuning options
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
