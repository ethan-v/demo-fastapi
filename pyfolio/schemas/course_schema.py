from typing import List, Optional
from pydantic import BaseModel
from pyfolio.schemas.course_lesson_schema import CourseLessonResponse


class CourseBase(BaseModel):
    title: str
    slug: str
    icon: str
    image: str
    description: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]


class CourseCreate(CourseBase):
    title: str
    slug: Optional[str]
    icon: Optional[str]
    image: Optional[str]
    description: str
    is_active: bool


class CourseUpdate(CourseBase):
    title: Optional[str]
    slug: Optional[str]
    icon: Optional[str]
    image: Optional[str]
    description: Optional[str]
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    id: int
    models: List[CourseLessonResponse] = []

    class Config:
        orm_mode = True
