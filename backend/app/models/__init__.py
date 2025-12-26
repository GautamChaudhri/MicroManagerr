# ============================================================================
# MicroManagerr - Models Package
# ============================================================================
# This package contains SQLAlchemy database models.
#
# WHAT IS A MODEL?
# A model is a Python class that represents a database table.
# Each instance of the class represents a row in that table.
#
# EXAMPLE:
#   class MediaFile(Base):
#       __tablename__ = "media_files"
#       id = Column(Integer, primary_key=True)
#       path = Column(String, unique=True)
#       has_hdr = Column(Boolean)
#
# This creates a table "media_files" with columns: id, path, has_hdr
#
# We'll add models in Phase 1 when we set up the database.
# ============================================================================
