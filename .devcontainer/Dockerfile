# =============================================================================
# MicroManagerr Development Container
# =============================================================================
# This Dockerfile creates a complete development environment with all tools
# needed to develop, test, and debug MicroManagerr.
#
# Includes:
# - Python 3.11 with pip and venv
# - FFmpeg (media analysis and processing)
# - MediaInfo (detailed media metadata extraction)
# - MKVToolNix (MKV file manipulation)
# - Git, curl, and other development utilities
# =============================================================================

FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# =============================================================================
# Install system dependencies
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Media analysis tools
    ffmpeg \
    mediainfo \
    mkvtoolnix \
    # Build essentials (for compiling Python packages)
    build-essential \
    # Useful utilities
    curl \
    wget \
    jq \
    # PostgreSQL client (for database operations)
    postgresql-client \
    # Clean up apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# Python environment setup
# =============================================================================
# Upgrade pip to latest version
RUN pip install --upgrade pip

# Install global Python tools that are useful during development
RUN pip install --no-cache-dir \
    # Code formatting and linting
    ruff \
    # Type checking
    mypy \
    # Testing
    pytest \
    pytest-cov \
    pytest-asyncio \
    # Interactive debugging
    ipython \
    # HTTP debugging
    httpie

# =============================================================================
# Environment configuration
# =============================================================================
# Set Python to run unbuffered (better for Docker logs)
ENV PYTHONUNBUFFERED=1

# Don't write .pyc files (cleaner development)
ENV PYTHONDONTWRITEBYTECODE=1

# Add local bin to PATH for user-installed packages
ENV PATH="/home/vscode/.local/bin:${PATH}"

# Set the default working directory
WORKDIR /workspace

# =============================================================================
# Post-create setup will be handled by devcontainer.json
# =============================================================================
