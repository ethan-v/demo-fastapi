from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pyfolio.models.db import init_db
from pyfolio.configs.app import appConfigs
from pyfolio.middlewares import ROUTES_MIDDLEWARE
from pyfolio.routers.v1.router_v1 import router_v1
from pyfolio.routers.v2.router_v2 import router_v2
from pyfolio.routers.admin.router_admin import router_admin

app = FastAPI(
    title="Pyfolio API",
    description="Opensource Portfolio Application",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Github",
        "url": "https://github.com/ethanvu-dev/pyfolio",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    middleware=ROUTES_MIDDLEWARE,
)
app.mount(appConfigs.STATICS_ROUTE, StaticFiles(directory=appConfigs.STATICS_DIRECTORY), name="static")

templates = Jinja2Templates(directory=f"{appConfigs.FRONT_TEMPLATE_PATH}")


@app.on_event("startup")
async def startup_event():
    init_db()


@app.on_event("shutdown")
def shutdown_event():
    with open("app.log", mode="a") as log:
        log.write("Application shutdown")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Register APIs
app.include_router(router_admin)
app.include_router(router_v1)
app.include_router(router_v2)
