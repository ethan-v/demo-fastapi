from typing import Optional
from pydantic import BaseModel


class CourseLessonBase(BaseModel):
    title: str
    slug: str
    image: str
    content: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]


class CourseLessonCreate(CourseLessonBase):
    category_id: int


class CourseLessonUpdate(CourseLessonBase):
    title: Optional[str]
    slug: Optional[str]
    image: Optional[str]
    content: Optional[str]
    category_id: Optional[int]
    is_active: Optional[bool]


class CourseLessonResponse(CourseLessonBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True
