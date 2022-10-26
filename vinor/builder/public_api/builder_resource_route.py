from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from vinor.builder.base.base_response import SuccessResponse
from vinor.builder.dependencies import get_db
from vinor.builder.public_api.builder_service import BuilderService

router = APIRouter()


@router.get("/{table}/list")
def read_resource_list(table: str, db: Session = Depends(get_db)):
    resource_data_list = BuilderService(db).load_resource_data_as_list(table_name=table)
    return SuccessResponse(
        message=f'Retrieve {table} successfully',
        data=resource_data_list,
    )


@router.get("/{table}/detail/{id}")
def read_resource_detail(table: str, id: int, db: Session = Depends(get_db)):
    resource_data_detail = BuilderService(db).load_resource_data_as_detail(table_name=table, field_id=id)
    return SuccessResponse(
        message=f'Retrieve {table} successfully',
        data=resource_data_detail
    )


@router.post("/{table}")
def create_resource_data(table: str, data: dict, db: Session = Depends(get_db)):
    resource_data_created = BuilderService(db).create_resource_data(table_name=table, data=data)
    return SuccessResponse(
        message=f'Created {table} successfully',
        data=resource_data_created
    )


@router.put("/{table}/{id}")
def update_resource_data(table: str, id: int, data: dict, db: Session = Depends(get_db)):
    print(f"update_resource_data(): table={table}, id={id}, data={data}")
    resource_data_detail = BuilderService(db).load_resource_data_as_detail(table_name=table, field_id=id)
    if resource_data_detail is None:
        raise HTTPException(status_code=404, detail=f"{table} not found")
    resource_data_updated = BuilderService(db).update_resource_data(table_name=table, field_id=id, data=data)
    return SuccessResponse(
        message=f'Updated {table} successfully',
        data=resource_data_updated
    )
