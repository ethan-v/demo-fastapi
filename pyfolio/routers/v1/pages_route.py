from typing import Union

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pyfolio.dependencies import get_db
from pyfolio.repositories.page_repository import PageRepository
from pyfolio.schemas.base_response_schema import SuccessResponse
from pyfolio.schemas.page_schema import PageCreate, PageUpdate

router = APIRouter()


@router.get("")
def read_pages(skip: int = 0, limit: int = 10, sort: str = 'id', order='desc',
               search_by: str = '', search_value: str = '',
               db: Session = Depends(get_db)):
    pages = PageRepository(db).paginate(
        skip=skip,
        limit=limit,
        sort=sort,
        order=order,
        search_by=search_by,
        search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve pages successfully',
        data=pages
    )


@router.get("/{idOrSlug}")
def read_page(idOrSlug: Union[int, str], db: Session = Depends(get_db)):
    if isinstance(idOrSlug, str):
        page = PageRepository(db).find_by_slug(slug=idOrSlug)
    else:
        page = PageRepository(db).find(id=idOrSlug)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    return SuccessResponse(
        message='Retrieve page successfully',
        data=page
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_page(page: PageCreate, db: Session = Depends(get_db)):
    db_page = PageRepository(db).find_by_title(page.title)
    if db_page:
        raise HTTPException(status_code=400, detail="Title already exists")
    page = PageRepository(db).create(page)
    if page is None:
        raise HTTPException(status_code=500, detail="Failed to create page")
    else:
        return SuccessResponse(
            message='Created page',
            data=page
        )


@router.put("/{id}")
def update_page(id: int, page: PageUpdate, db: Session = Depends(get_db)):
    db_page = PageRepository(db).find(id)
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    page_data = page.dict(exclude_unset=True)
    print(page_data)
    for key, value in page_data.items():
        setattr(db_page, key, value)
    page = PageRepository(db).update(db_page)
    return SuccessResponse(
        message='Updated page',
        data=page
    )


@router.delete("/{id}")
def delete_page(id: int, db: Session = Depends(get_db)):
    db_page = PageRepository(db).find(id)
    if db_page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    PageRepository(db).delete(db_page)
    return {
        "message": "Page was deleted successfully."
    }
