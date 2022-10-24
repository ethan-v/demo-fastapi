from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vinor.builder.base.base_response import SuccessResponse
from vinor.builder.dependencies import get_db
from vinor.builder.public_api.builder_service import BuilderService

router = APIRouter()


@router.get("/{table}/list")
def read_resource_list(table: str, db: Session = Depends(get_db)):
    schemas = BuilderService(db).load_resource_data_as_list(table_name=table)
    return SuccessResponse(
        message=f'Retrieve {table} successfully',
        data=schemas,
    )


@router.get("/{table}/detail/{id}")
def read_resource_detail(table: str, id: int, db: Session = Depends(get_db)):
    schemas = BuilderService(db).load_resource_data_as_detail(table_name=table, field_id=id)
    return SuccessResponse(
        message=f'Retrieve {table} successfully',
        data=schemas,
    )


@router.post("/{table}")
def create_resource_data(table: str, data: dict, db: Session = Depends(get_db)):
    resource_data = BuilderService(db).create_resource_data(table_name=table, data=data)
    # resource_data = data
    return SuccessResponse(
        message=f'Created {table} successfully',
        data=resource_data,
        debug=f"Create resource data for {table}"
    )
