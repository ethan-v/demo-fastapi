from fastapi import APIRouter
from pyfolio.routers.admin import dashboard, post

router_admin = APIRouter(prefix="/admin")
router_admin.include_router(dashboard.router, tags=["Admin - Dashboard"])
router_admin.include_router(post.router, tags=["Admin - Post"])
