from os import getcwd
from pydantic import BaseSettings

BASE_PATH: str = getcwd()


class AppConfigs(BaseSettings):

    APP_PATH: str = getcwd()
    STATICS_DIRECTORY: str = 'pyfolio/static'
    STATICS_ROUTE: str = '/static'
    STATICS_PATH: str = f'{BASE_PATH}/{STATICS_DIRECTORY}'


appConfigs = AppConfigs()
