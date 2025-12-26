# ============================================================================
# MicroManagerr - Production Dockerfile
# ============================================================================
# This Dockerfile creates a production-ready container for MicroManagerr.
#
# WHAT IS A DOCKERFILE?
# A Dockerfile is a recipe for building a Docker image. It specifies:
# - What base image to start from
# - What to install
# - What files to copy
# - What command to run
#
# HOW TO USE:
# Build:  docker build -t micromanagerr -f docker/Dockerfile .
# Run:    docker run -p 8000:8000 micromanagerr
#
# MULTI-STAGE BUILD EXPLAINED:
# We use two stages to create a smaller final image:
# 1. Builder stage: Installs all dependencies (including dev tools)
# 2. Runtime stage: Copies only what's needed to run
#
# This reduces the final image size significantly!
# ============================================================================

# =============================================================================
# Stage 1: Builder
# =============================================================================
# This stage prepares all dependencies. It's discarded after building.

FROM python:3.12-slim as builder

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files
# PYTHONUNBUFFERED: Don't buffer stdout/stderr (see logs immediately)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # pip configuration
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
# These are only needed during installation, not at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
# This keeps our dependencies isolated and makes the multi-stage build cleaner
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /build
COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt


# =============================================================================
# Stage 2: Runtime
# =============================================================================
# This is the final image that will be deployed.
# It only contains what's needed to run the application.

FROM python:3.12-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Add virtual environment to PATH
    PATH="/opt/venv/bin:$PATH" \
    # Application settings
    HOST=0.0.0.0 \
    PORT=8000

# Install runtime dependencies
# These are needed at runtime (e.g., ffmpeg for media analysis)
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Media analysis tools (uncomment in Phase 2)
    # ffmpeg \
    # mediainfo \
    # mkvtoolnix \
    # Health check utility
    curl \
    && rm -rf /var/lib/apt/lists/* \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
# Running as root in containers is a security risk!
RUN groupadd --gid 1000 micromanagerr && \
    useradd --uid 1000 --gid micromanagerr --shell /bin/bash --create-home micromanagerr

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Copy application code
COPY backend/app ./app

# Create data directory for SQLite database
RUN mkdir -p /app/data && chown -R micromanagerr:micromanagerr /app

# Switch to non-root user
USER micromanagerr

# Expose the port the app runs on
EXPOSE 8000

# Health check
# Docker will periodically run this command to check if the container is healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
# Using exec form (recommended) - passes signals properly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# =============================================================================
# LEARNING NOTES
# =============================================================================
#
# DOCKER LAYER CACHING:
# Each instruction creates a layer. Docker caches layers and reuses them
# if nothing changed. To optimize build times:
# - Put things that change rarely at the top (OS, dependencies)
# - Put things that change often at the bottom (your code)
# - Copy requirements.txt separately from code (deps cached if only code changes)
#
# SECURITY BEST PRACTICES:
# - Use specific version tags (python:3.12-slim not python:latest)
# - Run as non-root user
# - Use slim/alpine base images
# - Don't install unnecessary packages
# - Remove package manager caches
#
# DEBUGGING A CONTAINER:
# docker run -it micromanagerr /bin/bash
# This gives you a shell inside the container to poke around
# =============================================================================
