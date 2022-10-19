from typing import Optional
from pydantic import BaseModel


class SchemaBase(BaseModel):
    name: str
    is_active: bool
    created_at: Optional[str]
    updated_at: Optional[str]


class SchemaCreate(SchemaBase):
    name: str
    is_active: bool


class SchemaUpdate(SchemaBase):
    name: Optional[str]
    is_active: Optional[bool]


class SchemaResponse(SchemaBase):
    id: int
    # fields: List[FieldResponse] = []

    class Config:
        orm_mode = True
