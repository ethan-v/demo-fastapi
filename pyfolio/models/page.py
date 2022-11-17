from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import DBModel


class Page(DBModel):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(190), unique=True, index=True)
    slug = Column(String(190), unique=True, index=True)
    image = Column(String(190), default=None)
    excerpt = Column(String(500), default=None)
    content = Column(Text, default=None)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
