from pydantic import BaseModel


class BuilderSetting(BaseModel):

    VERSION: str = '1.0.0'
    API_TEMPLATE_PATH: str = ''
    UI_TEMPLATE_PATH: str = ''


builderSettings = BuilderSetting
