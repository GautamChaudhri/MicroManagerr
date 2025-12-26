# ============================================================================
# MicroManagerr - Configuration Management
# ============================================================================
# This module handles all application configuration.
#
# WHY CENTRALIZE CONFIGURATION?
# 1. Single source of truth - all settings in one place
# 2. Environment-specific settings - different values for dev/prod
# 3. Secrets management - keep API keys out of code
# 4. Type safety - Pydantic validates all settings
#
# HOW IT WORKS:
# 1. Pydantic Settings reads from environment variables
# 2. It can also read from a .env file (for local development)
# 3. Settings are validated when the app starts
# 4. If required settings are missing, the app fails fast with a clear error
# ============================================================================

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Find the project root directory (where .env file lives)
# This file is at: backend/app/config.py
# Project root is: ../../ (two levels up)
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Pydantic Settings automatically:
    - Reads environment variables matching field names (case-insensitive)
    - Converts types (e.g., "8000" string -> 8000 integer)
    - Validates values
    - Provides defaults where specified

    Environment variables can be set in:
    - System environment (production)
    - .env file (development)
    - docker-compose.yml (Docker deployment)
    """

    # -------------------------------------------------------------------------
    # Application Settings
    # -------------------------------------------------------------------------

    # The name of our application
    app_name: str = "MicroManagerr"

    # Debug mode - enables extra logging and error details
    # IMPORTANT: Always False in production!
    debug: bool = False

    # The host to bind to (0.0.0.0 = all interfaces)
    host: str = "0.0.0.0"

    # The port to run on
    port: int = 8000

    # -------------------------------------------------------------------------
    # Database Settings
    # -------------------------------------------------------------------------

    # Database URL in SQLAlchemy format
    # SQLite example: sqlite+aiosqlite:///./data/micromanagerr.db
    # PostgreSQL example: postgresql+asyncpg://user:pass@localhost/dbname
    database_url: str = "sqlite+aiosqlite:///./data/micromanagerr.db"

    # -------------------------------------------------------------------------
    # Sonarr Configuration
    # -------------------------------------------------------------------------

    # These are Optional because users might not have Sonarr
    # They'll configure these through the UI later, but we support env vars too

    sonarr_url: Optional[str] = Field(
        default=None,
        description="Sonarr base URL, e.g., http://localhost:8989"
    )

    sonarr_api_key: Optional[str] = Field(
        default=None,
        description="Sonarr API key from Settings -> General"
    )

    # -------------------------------------------------------------------------
    # Radarr Configuration
    # -------------------------------------------------------------------------

    radarr_url: Optional[str] = Field(
        default=None,
        description="Radarr base URL, e.g., http://localhost:7878"
    )

    radarr_api_key: Optional[str] = Field(
        default=None,
        description="Radarr API key from Settings -> General"
    )

    # -------------------------------------------------------------------------
    # Logging Configuration
    # -------------------------------------------------------------------------

    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_level: str = "INFO"

    # -------------------------------------------------------------------------
    # Pydantic Settings Configuration
    # -------------------------------------------------------------------------

    model_config = SettingsConfigDict(
        # Path to the .env file (in project root, not backend/)
        env_file=ENV_FILE_PATH,

        # Encoding of the .env file
        env_file_encoding="utf-8",

        # Whether .env file overrides system environment variables
        # False = system env vars take priority (good for Docker)
        env_file_override=False,

        # Make field names case-insensitive for env vars
        # So DATABASE_URL and database_url both work
        case_sensitive=False,

        # Allow extra fields (useful for forward compatibility)
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Validators
    # -------------------------------------------------------------------------

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Ensure log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        upper_v = v.upper()
        if upper_v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return upper_v

    # -------------------------------------------------------------------------
    # Computed Properties
    # -------------------------------------------------------------------------

    @property
    def sonarr_configured(self) -> bool:
        """Check if Sonarr is configured."""
        return bool(self.sonarr_url and self.sonarr_api_key)

    @property
    def radarr_configured(self) -> bool:
        """Check if Radarr is configured."""
        return bool(self.radarr_url and self.radarr_api_key)


# =============================================================================
# Settings Singleton
# =============================================================================
# We use @lru_cache to ensure settings are only loaded once.
# This is called a "singleton pattern" - there's only ever one Settings object.
#
# WHY?
# 1. Performance - don't re-read .env file on every request
# 2. Consistency - all parts of the app see the same settings
# 3. Early failure - if settings are invalid, app fails at startup, not later
# =============================================================================

@lru_cache
def get_settings() -> Settings:
    """
    Get the application settings.

    This function is cached, so settings are only loaded once.
    Call this whenever you need access to configuration.

    Usage:
        from app.config import get_settings

        settings = get_settings()
        print(settings.app_name)
    """
    return Settings()


# For convenience, you can also import settings directly
# (This runs when the module is first imported)
settings = get_settings()
