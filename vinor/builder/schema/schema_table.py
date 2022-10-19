from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func

from vinor.builder.database import BuilderDBModel


class SchemaTable(BuilderDBModel):
    """
    Builder schemas table
    """
    __tablename__ = "builder_schemas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
