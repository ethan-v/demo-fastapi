from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from pyfolio.apps.builder.dependencies import get_db
from pyfolio.apps.builder.base.base_response import SuccessResponse

from .builder_schema_repository import BuilderSchemaRepository
from .builder_schema_models import BuilderSchemaCreate, BuilderSchemaUpdate

router = APIRouter()


@router.get("/")
def read_builder_schemas(
    skip: int = 0, limit: int = 10, order_by: str = 'id', order_direct='desc', search_by: str = '', search_value: str = '',
    db: Session = Depends(get_db)
):
    schemas = BuilderSchemaRepository(db).paginate(
        skip=skip, limit=limit,
        order_by=order_by, order_direct=order_direct,
        search_by=search_by, search_value=search_value
    )
    return SuccessResponse(
        message='Retrieve schema successfully',
        data=schemas
    )


@router.get("/{id}")
def read_builder_schema(id: int, db: Session = Depends(get_db)):
    schema = BuilderSchemaRepository(db).find(id)
    if schema is None:
        raise HTTPException(status_code=404, detail="BuilderSchema not found")
    return SuccessResponse(
        message='Retrieve car brand successfully',
        data=schema
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_builder_schema(schema: BuilderSchemaCreate, db: Session = Depends(get_db)):
    db_schema = BuilderSchemaRepository(db).find_by_name(schema.name)
    if not db_schema:
        db_schema = BuilderSchemaRepository(db).create(schema)
    if db_schema is None:
        raise HTTPException(status_code=500, detail="Failed to create BuilderSchema")
    else:
        return SuccessResponse(
            message='Created BuilderSchema',
            data=db_schema,
        )


@router.put("/{id}")
def update_builder_schema(id: int, schema: BuilderSchemaUpdate, db: Session = Depends(get_db)):
    db_builder_schema = BuilderSchemaRepository(db).find(id)
    if db_builder_schema is None:
        raise HTTPException(status_code=404, detail="BuilderSchema not found")
    schema_data = schema.dict(exclude_unset=True)
    for key, value in schema_data.items():
        setattr(db_builder_schema, key, value)
    schema = BuilderSchemaRepository(db).update(db_builder_schema)
    return SuccessResponse(
        message='Updated BuilderSchema',
        data=schema,
    )


@router.delete("/{id}")
def delete_builder_schema(id: int, db: Session = Depends(get_db)):
    db_builder_schema = BuilderSchemaRepository(db).find(id)
    if db_builder_schema is None:
        raise HTTPException(status_code=404, detail="BuilderSchema not found")
    BuilderSchemaRepository(db).delete(db_builder_schema)
    return {
        "message": "BuilderSchema was deleted successfully."
    }
