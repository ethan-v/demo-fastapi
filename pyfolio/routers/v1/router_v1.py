from fastapi import APIRouter
from pyfolio.routers.v1 import root_route, files_route, categories_route, posts_route


router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(root_route.router, tags=["Root"])
router_v1.include_router(files_route.router, prefix="/files", tags=["Files"])
router_v1.include_router(categories_route.router, prefix="/categories", tags=["Category"])
router_v1.include_router(posts_route.router, prefix="/posts", tags=["Post"])
