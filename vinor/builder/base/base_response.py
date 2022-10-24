from pydantic import BaseModel
from typing import Any, Optional, List


class SuccessResponse(BaseModel):
    message: str = ''
    data: Optional[Any] = None


class PaginationResponse(BaseModel):
    total: int
    limit: int
    skip: int = 0
    total_page: int
    next_page_link: str = None
    items: List = []
