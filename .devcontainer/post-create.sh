#!/bin/bash
# =============================================================================
# Post-Create Script for MicroManagerr Dev Container
# =============================================================================
# This script runs once when the dev container is first created.
# It sets up the Python virtual environment and installs all dependencies.
# =============================================================================

set -e  # Exit on any error

echo "=========================================="
echo "  MicroManagerr Dev Container Setup"
echo "=========================================="

# Navigate to workspace
cd /workspace

# =============================================================================
# Create Python virtual environment
# =============================================================================
echo ""
echo "📦 Creating Python virtual environment..."
python -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# =============================================================================
# Install dependencies
# =============================================================================
echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# =============================================================================
# Setup environment file
# =============================================================================
cd /workspace
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "   ⚠️  Remember to edit .env with your Sonarr/Radarr API keys!"
fi

# =============================================================================
# Verify installations
# =============================================================================
echo ""
echo "🔍 Verifying installed tools..."
echo ""

echo "Python:    $(python --version)"
echo "Pip:       $(pip --version | cut -d' ' -f1-2)"
echo "FFmpeg:    $(ffmpeg -version 2>&1 | head -1)"
echo "MediaInfo: $(mediainfo --version 2>&1 | head -1)"
echo "MKVMerge:  $(mkvmerge --version 2>&1 | head -1)"

# =============================================================================
# Done!
# =============================================================================
echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start developing:"
echo "  1. cd backend"
echo "  2. source ../venv/bin/activate"
echo "  3. uvicorn app.main:app --reload"
echo ""
echo "Then visit: http://localhost:8000/docs"
echo ""
echo "Don't forget to edit .env with your API keys!"
echo "=========================================="
