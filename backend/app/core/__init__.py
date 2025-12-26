# ============================================================================
# MicroManagerr - Core Package
# ============================================================================
# This package contains core business logic that isn't tied to the API layer.
#
# WHAT GOES HERE:
# - arr_client.py: HTTP client for Sonarr/Radarr APIs
# - media_analyzer.py: FFmpeg/MediaInfo integration for file analysis
# - tag_manager.py: Logic for creating and applying tags
#
# WHY SEPARATE FROM API?
# Keeping business logic separate from HTTP handling allows:
# 1. Easier testing (no need to mock HTTP requests)
# 2. Reuse in different contexts (CLI, background jobs, etc.)
# 3. Cleaner, more focused code in each layer
# ============================================================================
