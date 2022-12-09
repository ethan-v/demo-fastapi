from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pyfolio.configs.app import appConfigs

templates = Jinja2Templates(directory=f"{appConfigs.ADMIN_TEMPLATE_PATH}/theme/default")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

