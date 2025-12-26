# ============================================================================
# MicroManagerr - Tests Package
# ============================================================================
# This package contains all tests for the application.
#
# TESTING PHILOSOPHY
# Good tests are:
# 1. Fast - Run in seconds, not minutes
# 2. Isolated - Don't depend on external services
# 3. Repeatable - Same result every time
# 4. Self-checking - Pass or fail automatically
#
# TEST ORGANIZATION:
# tests/
#   conftest.py          - Shared fixtures (reusable test setup)
#   test_api/
#     test_health.py     - Tests for health endpoints
#     test_sonarr.py     - Tests for Sonarr endpoints
#   test_services/
#     test_scanner.py    - Tests for scanner service
#   test_core/
#     test_analyzer.py   - Tests for media analyzer
#
# HOW TO RUN TESTS:
#   pytest                    # Run all tests
#   pytest -v                 # Verbose output
#   pytest tests/test_api/    # Run only API tests
#   pytest -k "test_health"   # Run tests matching pattern
# ============================================================================
