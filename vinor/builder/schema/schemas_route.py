from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from vinor.builder.dependencies import get_db
from vinor.builder.base.base_response import SuccessResponse

from .schema_repository import SchemaRepository
from .schema_models import SchemaCreate, SchemaUpdate

router = APIRouter()


@router.get("/")
def read_schemas(
    skip: int = 0, limit: int = 10, order_by: str = 'id', order_direct='desc', search_by: str = '', search_value: str = '',
    db: Session = Depends(get_db)
):
    schemas = SchemaRepository(db).paginate(
        skip=skip, limit=limit,
        order_by=order_by, order_direct=order_direct,
        search_by=search_by, search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve schema successfully',
        data=schemas
    )


@router.get("/{id}")
def read_schema(id: int, db: Session = Depends(get_db)):
    schema = SchemaRepository(db).find(id)
    if schema is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    return SuccessResponse(
        message='Retrieve car brand successfully',
        data=schema
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_schema(schema: SchemaCreate, db: Session = Depends(get_db)):
    db_schema = SchemaRepository(db).find_by_name(schema.name)
    if db_schema:
        raise HTTPException(status_code=400, detail="Name already exists")
    schema = SchemaRepository(db).create(schema)
    if schema is None:
        raise HTTPException(status_code=500, detail="Failed to create Schema")
    else:
        return SuccessResponse(
            message='Created Schema',
            data=schema,
        )


@router.put("/{id}")
def update_schema(id: int, schema: SchemaUpdate, db: Session = Depends(get_db)):
    db_schema = SchemaRepository(db).find(id)
    if db_schema is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(db_schema, key, value)
    schema = SchemaRepository(db).update(db_schema)
    return SuccessResponse(
        message='Updated Schema',
        data=schema,
    )


@router.delete("/{id}")
def delete_schema(id: int, db: Session = Depends(get_db)):
    db_schema = SchemaRepository(db).find(id)
    if db_schema is None:
        raise HTTPException(status_code=404, detail="Schema not found")
    SchemaRepository(db).delete(db_schema)
    return {
        "message": "Schema was deleted successfully."
    }
