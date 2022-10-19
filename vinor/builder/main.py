from fastapi import FastAPI, APIRouter
from vinor.builder.schema import schemas_route

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Builder API!"}


builder_api = FastAPI()
builder_api.include_router(router)
builder_api.include_router(schemas_route.router, prefix="/schemas", tags=["Schema"])
