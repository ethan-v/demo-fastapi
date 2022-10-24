from typing import Optional
from pydantic import BaseModel


class BuilderDataBase(BaseModel):
    schema_name: str
    field_id: int
    field_name: str
    data: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class BuilderDataCreate(BuilderDataBase):
    pass


class BuilderDataUpdate(BuilderDataBase):
    data: Optional[str] = None

    class Config:
        fields = {
            'schema_name': {'exclude': True},
            'field_name': {'exclude': True}
        }


class BuilderDataResponse(BuilderDataBase):
    id: int

    class Config:
        orm_mode = True
