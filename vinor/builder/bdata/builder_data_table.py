from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from vinor.builder.database import BuilderDBModel


class BuilderDataTable(BuilderDBModel):
    __tablename__ = "builder_data"

    id = Column(Integer, primary_key=True, index=True)
    schema_name = Column(String(255), index=True)
    field_id = Column(Integer)
    field_name = Column(String(255), index=True)
    data = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
