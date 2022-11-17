from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from .db import DBModel


class Setting(DBModel):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(190), unique=True)
    key = Column(String(190))
    value = Column(Text)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
