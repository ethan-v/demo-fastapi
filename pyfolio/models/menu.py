from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func

from .db import DBModel


class Menu(DBModel):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    group = Column(String(190))
    title = Column(String(190), unique=True)
    url = Column(String(190))
    target = Column(String(190), default="")
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
