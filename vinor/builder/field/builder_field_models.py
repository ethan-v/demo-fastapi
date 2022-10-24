from typing import Optional
from pydantic import BaseModel


class BuilderFieldBase(BaseModel):
    name: str
    schema_name: str
    data_type: str
    default: Optional[str] = None
    relation_mapping: Optional[str] = None
    comment: Optional[str] = None
    is_required: bool
    in_request: bool
    in_request_name: Optional[str] = None
    in_response: bool
    in_response_name: Optional[str] = None
    callback_function: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class BuilderFieldCreate(BuilderFieldBase):
    pass


class BuilderFieldUpdate(BuilderFieldBase):
    name: Optional[str]
    schema_name: Optional[str]
    data_type: Optional[str]
    is_required: Optional[bool]
    in_request: Optional[bool]
    in_response: Optional[bool]


class BuilderFieldResponse(BuilderFieldBase):
    id: int

    class Config:
        orm_mode = True
