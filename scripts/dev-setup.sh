#!/bin/bash
# ============================================================================
# MicroManagerr - Development Environment Setup Script
# ============================================================================
# This script sets up your local development environment.
#
# WHAT IT DOES:
# 1. Creates a Python virtual environment
# 2. Installs all dependencies
# 3. Creates your .env file from the example
# 4. Creates the data directory
#
# HOW TO USE:
# chmod +x scripts/dev-setup.sh
# ./scripts/dev-setup.sh
# ============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "MicroManagerr Development Setup"
echo "=========================================="
echo ""

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Project directory: $PROJECT_ROOT"
echo ""

# Step 1: Check Python version
echo "[1/5] Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2)
    echo "      Found Python $PYTHON_VERSION"
else
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.11 or later from https://python.org"
    exit 1
fi

# Step 2: Create virtual environment
echo ""
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "      Virtual environment already exists."
else
    python3 -m venv venv
    echo "      Created: venv/"
fi

# Step 3: Activate and install dependencies
echo ""
echo "[3/5] Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r backend/requirements.txt --quiet
pip install -r backend/requirements-dev.txt --quiet
echo "      Dependencies installed."

# Step 4: Set up environment file
echo ""
echo "[4/5] Setting up environment file..."
if [ -f ".env" ]; then
    echo "      .env already exists (not overwriting)."
else
    cp .env.example .env
    echo "      Created .env from .env.example"
    echo ""
    echo "      IMPORTANT: Edit .env and add your Sonarr/Radarr API keys!"
fi

# Step 5: Create data directory
echo ""
echo "[5/5] Creating data directory..."
mkdir -p backend/data
echo "      Created: backend/data/"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Edit your configuration:"
echo "   nano .env"
echo "   (Add your SONARR_URL, SONARR_API_KEY, etc.)"
echo ""
echo "3. Run the development server:"
echo "   cd backend"
echo "   uvicorn app.main:app --reload"
echo ""
echo "4. Open your browser to:"
echo "   http://localhost:8000/docs"
echo ""
echo "Happy coding!"
