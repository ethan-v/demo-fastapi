from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from vinor.builder.dependencies import get_db
from vinor.builder.base.base_response import SuccessResponse

from .builder_field_repository import BuilderFieldRepository
from .builder_field_models import BuilderFieldCreate, BuilderFieldUpdate

router = APIRouter()


@router.get("/")
def read_fields(
    skip: int = 0, limit: int = 10, order_by: str = 'id', order_direct='desc', search_by: str = '', search_value: str = '',
    db: Session = Depends(get_db)
):
    fields = BuilderFieldRepository(db).paginate(
        skip=skip, limit=limit,
        order_by=order_by, order_direct=order_direct,
        search_by=search_by, search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve field successfully',
        data=fields
    )


@router.get("/{id}")
def read_field(id: int, db: Session = Depends(get_db)):
    field = BuilderFieldRepository(db).find(id)
    if field is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    return SuccessResponse(
        message='Retrieve car brand successfully',
        data=field
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_field(field: BuilderFieldCreate, db: Session = Depends(get_db)):
    db_field = BuilderFieldRepository(db).find_by_name_and_schema(schema_name=field.schema_name, name=field.name)
    if not db_field:
        db_field = BuilderFieldRepository(db).create(field)
    if db_field is None:
        raise HTTPException(status_code=500, detail="Failed to create schema field")
    else:
        return SuccessResponse(
            message='Created schema field',
            data=db_field,
        )


@router.put("/{id}")
def update_field(id: int, field: BuilderFieldUpdate, db: Session = Depends(get_db)):
    db_field = BuilderFieldRepository(db).find(id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    field_data = field.dict(exclude_unset=True)
    for key, value in field_data.items():
        setattr(db_field, key, value)
    field = BuilderFieldRepository(db).update(db_field)
    return SuccessResponse(
        message='Updated schema field',
        data=field,
    )


@router.delete("/{id}")
def delete_field(id: int, db: Session = Depends(get_db)):
    db_field = BuilderFieldRepository(db).find(id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    BuilderFieldRepository(db).delete(db_field)
    return {
        "message": "Schema was deleted successfully."
    }
