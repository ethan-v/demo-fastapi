from fastapi import FastAPI, APIRouter

from pyfolio.apps.builder.field import builder_fields_route
from pyfolio.apps.builder.schema import builder_schemas_route
from pyfolio.apps.builder.apis import builder_resource_route

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Builder API!"}


builder_api = FastAPI()
builder_api.include_router(router)
builder_api.include_router(builder_schemas_route.router, prefix="/schemas", tags=["Schema"])
builder_api.include_router(builder_fields_route.router, prefix="/fields", tags=["Field"])

# Public API Resources
builder_api.include_router(builder_resource_route.router, prefix="/resource", tags=["Dynamic Resource"])
