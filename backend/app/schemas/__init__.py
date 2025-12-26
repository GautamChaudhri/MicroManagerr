# ============================================================================
# MicroManagerr - Schemas Package
# ============================================================================
# This package contains Pydantic schemas for API data validation.
#
# MODELS vs SCHEMAS - What's the difference?
#
# MODELS (SQLAlchemy):
# - Define database structure
# - Used internally by the app
# - Tied to database operations
#
# SCHEMAS (Pydantic):
# - Define API request/response structure
# - Used for data validation
# - Serialization to/from JSON
#
# WHY BOTH?
# You often want different shapes for API vs database:
# - API response might exclude sensitive fields (passwords)
# - API request might be simpler than full database record
# - API might combine data from multiple tables
#
# EXAMPLE:
#   # Database model - has all fields
#   class User(Base):
#       id = Column(Integer, primary_key=True)
#       email = Column(String)
#       hashed_password = Column(String)  # Never expose this!
#       created_at = Column(DateTime)
#
#   # API schema - only safe fields
#   class UserResponse(BaseModel):
#       id: int
#       email: str
#       # No password or internal fields!
# ============================================================================
