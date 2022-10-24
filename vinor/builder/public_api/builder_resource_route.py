from typing import Optional, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from vinor.builder.base.base_response import SuccessResponse
from vinor.builder.dependencies import get_db
from vinor.builder.public_api.builder_service import BuilderService

router = APIRouter()


@router.get("")
def read_resource(
    tbl: str,
    view: Optional[str] = 'detail',
    db: Session = Depends(get_db)
):
    schemas = BuilderService(db).load_resource(table_name=tbl, view=view)
    return SuccessResponse(
        message=f'Retrieve {tbl} successfully',
        data=schemas,
        debug=f"view_model={view}"
    )


@router.post("/{tbl}")
def create_resource_data(tbl: str, data: dict, db: Session = Depends(get_db)):
    resource_data = BuilderService(db).create_resource_data(table_name=tbl, data=data)
    # resource_data = data
    return SuccessResponse(
        message=f'Created {tbl} successfully',
        data=resource_data,
        debug=f"Create resource data for {tbl}"
    )
