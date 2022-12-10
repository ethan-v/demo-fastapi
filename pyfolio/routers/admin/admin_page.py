from fastapi import Request
from fastapi.templating import Jinja2Templates
from pyfolio.configs.app import appConfigs

templates = Jinja2Templates(directory=f"{appConfigs.ADMIN_TEMPLATE_PATH}/theme/default")


class AdminPage:

    @staticmethod
    def render(request: Request, template_name: str, data: dict = {}):
        params = {
            "request": request,
            'app_name': appConfigs.APP_NAME,
        }
        params.update(data)
        return templates.TemplateResponse(template_name, params)

