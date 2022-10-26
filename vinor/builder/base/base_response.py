from pydantic import BaseModel, validator
from typing import Any, Optional, List


class SuccessResponse(BaseModel):
    message: str = ''
    data: Optional[Any] = None

    @validator('message', always=True)
    def set_default(cls, v: Optional[str]) -> str:
        if v is not None:
            return v.capitalize()
        return v


class PaginationResponse(BaseModel):
    total: int
    limit: int
    skip: int = 0
    total_page: int
    next_page_link: str = None
    items: List = []
