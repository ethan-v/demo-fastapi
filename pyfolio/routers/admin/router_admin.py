from fastapi import APIRouter
from pyfolio.routers.admin import dashboard, post, subscriber

router_admin = APIRouter(prefix="/admin")
router_admin.include_router(dashboard.router, tags=["Admin - Dashboard"])
router_admin.include_router(post.router, tags=["Admin - Post"])
router_admin.include_router(subscriber.router, tags=["Admin - Subscriber"])
