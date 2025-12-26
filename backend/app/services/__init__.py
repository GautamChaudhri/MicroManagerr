# ============================================================================
# MicroManagerr - Services Package
# ============================================================================
# This package contains high-level business logic services.
#
# WHAT IS A SERVICE?
# A service is a class or module that encapsulates complex business logic.
# It coordinates between different parts of the application.
#
# EXAMPLE - Scanner Service:
# The scanner service will:
# 1. Get list of files from Sonarr/Radarr
# 2. Call media analyzer for each file
# 3. Store results in database
# 4. Apply tags based on results
#
# This involves multiple components (API client, analyzer, database, tag manager)
# The service orchestrates them all.
#
# WHY SERVICES?
# 1. Keep API routes thin (they just call services)
# 2. Reusable logic (same service works for API, CLI, background jobs)
# 3. Testable (mock dependencies, test service logic)
# 4. Maintainable (one place for complex logic)
# ============================================================================
