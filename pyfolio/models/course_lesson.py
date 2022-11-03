from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import DBModel


class CourseLesson(DBModel):
    __tablename__ = "course_lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(190), unique=True, index=True)
    slug = Column(String(190), unique=True, index=True)
    image = Column(String(190), default=None)
    content = Column(String(190), default=None)
    video_url = Column(String(190), default=None)
    total_time = Column(String(190), default=None)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True,)
    course = relationship("Course", back_populates="lessons")
