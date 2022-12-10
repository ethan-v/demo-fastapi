from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from .admin_page import AdminPage


router = APIRouter()


@router.get("/subscribers", response_class=HTMLResponse)
async def read_item(request: Request):
    data = {
        'page_title': 'Subscribers',
    }
    return AdminPage.render(request, "pages/subscriber/index.html", data)

