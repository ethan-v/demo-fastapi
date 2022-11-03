from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pyfolio.apps.builder.database import BuilderDBModel


class BuilderResponse(BuilderDBModel):
    __tablename__ = "builder_responses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    field_mapping = Column(String(1000))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
