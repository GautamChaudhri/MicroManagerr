# ============================================================================
# MicroManagerr - App Package
# ============================================================================
# This file makes the 'app' directory a Python package.
#
# WHAT IS A PYTHON PACKAGE?
# In Python, a package is just a folder containing an __init__.py file.
# This allows you to import modules from this folder like:
#   from app.main import app
#   from app.config import settings
#
# The __init__.py can be empty (like this one mostly is) or can contain
# initialization code that runs when the package is imported.
# ============================================================================

# Version of the application
# Following Semantic Versioning: MAJOR.MINOR.PATCH
# - MAJOR: Breaking changes
# - MINOR: New features (backwards compatible)
# - PATCH: Bug fixes (backwards compatible)
__version__ = "0.1.0"
