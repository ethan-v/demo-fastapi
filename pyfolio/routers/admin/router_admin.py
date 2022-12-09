from fastapi import APIRouter
from pyfolio.routers.admin import root_route

router_admin = APIRouter(prefix="/admin")
router_admin.include_router(root_route.router, tags=["Admin - Root"])
# router_admin.include_router(items_route.router, prefix="/items", tags=["V2 - Item"])
