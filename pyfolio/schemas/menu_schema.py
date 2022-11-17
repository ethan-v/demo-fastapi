from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    title: str
    group: str
    url: str
    target: Optional[str]
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    title: Optional[str]
    group: Optional[str]
    url: Optional[str]
    target: Optional[str]
    is_active: Optional[bool]


class MenuResponse(MenuBase):
    id: int

    class Config:
        orm_mode = True
