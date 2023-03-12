from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pyfolio.models.db import init_db
from pyfolio.configs.app import appConfigs
from pyfolio.routers.v1.router_v1 import router_v1
from pyfolio.routers.v2.router_v2 import router_v2
from pyfolio.middlewares import ROUTES_MIDDLEWARE
from pyfolio.apps.builder import init_builder, builder_api

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
app.mount('/static', StaticFiles(), name="static")

# Integrate Builder API at: http://localhost:8000/builder/docs
app.mount("/builder", builder_api)


@app.on_event("startup")
async def startup_event():
    init_db()
    init_builder(embedded_app_name='Pyfolio', embedded_app_configs=appConfigs)


@app.on_event("shutdown")
def shutdown_event():
    with open("app.log", mode="a") as log:
        log.write("Application shutdown")


# Register APIs
app.include_router(router_v1)
app.include_router(router_v2)
