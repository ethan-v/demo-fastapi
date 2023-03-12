from typing import Optional
from pydantic import BaseModel, Extra


class BuilderSchemaBase(BaseModel):
    name: str
    is_active: bool = False
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        extra = Extra.allow


class BuilderSchemaCreate(BuilderSchemaBase):
    name: str
    is_active: Optional[bool] = False


class BuilderSchemaUpdate(BuilderSchemaBase):
    name: Optional[str]
    is_active: Optional[bool]


class BuilderSchemaResponse(BuilderSchemaBase):
    id: int
    # fields: List[FieldResponse] = []

    class Config:
        orm_mode = True
