from pydantic import BaseModel


class BuilderConfig(BaseModel):

    VERSION: str = '1.0.0'
    API_TEMPLATE_PATH: str = ''
    UI_TEMPLATE_PATH: str = ''


builderConfigs = BuilderConfig
