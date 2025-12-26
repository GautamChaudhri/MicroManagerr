# ============================================================================
# MicroManagerr - API Routes Package
# ============================================================================
# This package contains individual route modules.
# Each module handles a specific feature area of the API.
#
# HOW FASTAPI ROUTING WORKS:
# 1. Each route module creates an APIRouter instance
# 2. Endpoints are decorated with @router.get(), @router.post(), etc.
# 3. In main.py, routers are included with app.include_router()
# 4. FastAPI combines everything into one cohesive API
#
# EXAMPLE:
#   # In routes/health.py:
#   router = APIRouter()
#
#   @router.get("/health")
#   def health_check():
#       return {"status": "ok"}
#
#   # In main.py:
#   app.include_router(health.router)
#
# This pattern keeps code organized and makes features easy to find.
# ============================================================================

from app.api.routes import health, sonarr, radarr

__all__ = ["health", "sonarr", "radarr"]
