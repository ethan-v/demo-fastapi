from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from pyfolio.repositories.menu_repository import MenuRepository
from pyfolio.dependencies import get_db
from pyfolio.schemas.menu_schema import MenuCreate, MenuUpdate
from pyfolio.schemas.base_response_schema import SuccessResponse


router = APIRouter()


@router.get("")
def read_menus(
    skip: int = 0, limit: int = 10, sort: str = 'id', order='desc', search_by: str = '', search_value: str = '',
    db: Session = Depends(get_db)
):
    menus = MenuRepository(db).paginate(
        skip=skip, limit=limit,
        sort=sort, order=order,
        search_by=search_by, search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve menus successfully',
        data=menus
    )


@router.get("/{id}")
def read_menu(id: int, db: Session = Depends(get_db)):
    menu = MenuRepository(db).find(id)
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    return SuccessResponse(
        message='Retrieve menu successfully',
        data=menu
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_menu(menu: MenuCreate, db: Session = Depends(get_db)):
    db_menu = MenuRepository(db).find_by_title(menu.title)
    if db_menu:
        raise HTTPException(status_code=400, detail="Name already exists")
    # db_menu = MenuRepository(db).find_by_key(menu.key)
    # if db_menu:
    #     raise HTTPException(status_code=400, detail="Key already exists")
    menu = MenuRepository(db).create(menu)
    if menu is None:
        raise HTTPException(status_code=500, detail="Failed to create Menu")
    else:
        return SuccessResponse(
            message='Created Menu',
            data=menu,
        )


@router.put("/{id}")
def update_menu(id: int, menu: MenuUpdate, db: Session = Depends(get_db)):
    db_menu = MenuRepository(db).find(id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    menu = MenuRepository(db).update(db_menu)
    return SuccessResponse(
        message='Updated Menu',
        data=menu,
    )


@router.delete("/{id}")
def delete_menu(id: int, db: Session = Depends(get_db)):
    db_menu = MenuRepository(db).find(id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    MenuRepository(db).delete(db_menu)
    return {
        "message": "Menu was deleted successfully."
    }
