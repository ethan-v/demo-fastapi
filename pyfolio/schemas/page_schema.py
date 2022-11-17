from typing import Optional
from pydantic import BaseModel


class PageBase(BaseModel):
    title: str
    slug: Optional[str] = None
    image: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = False
    created_at: Optional[str]
    updated_at: Optional[str]


class PageCreate(PageBase):
    pass


class PageUpdate(PageBase):
    title: Optional[str]
    slug: Optional[str]
    image: Optional[str]
    excerpt: Optional[str]
    content: Optional[str]
    is_active: Optional[bool]


class PageResponse(PageBase):
    id: int

    class Config:
        orm_mode = True
