from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.sql import func

from pyfolio.apps.builder.database import BuilderDBModel


class BuilderDataTable(BuilderDBModel):
    __tablename__ = "builder_data"

    id = Column(Integer, primary_key=True, index=True)
    schema_name = Column(String(255), index=True)
    field_id = Column(BIGINT(unsigned=True), index=True)
    unique_fields = Column(String(255), index=True)
    data = Column(Text())
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
