import os
from pathlib import Path    # Python 3.6+ only
from pydantic import BaseSettings, Field

PROJECT_PATH: str = os.getcwd()
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = "{0}".format(Path(CURRENT_DIR).parent.parent)
ENV_PATH = "{0}/.env".format(PROJECT_PATH)
PROJECT_DIR = 'pyfolio'


class AppConfigs(BaseSettings):

    PROJECT_PATH: str = PROJECT_PATH
    APP_PATH: str = f'{PROJECT_PATH}/{PROJECT_DIR}'
    APP_NAME: str = Field('Portfolio', env='APP_NAME')
    APP_ENV: str = Field('', env='APP_ENV')
    APP_KEY: str = Field('', env='APP_KEY')
    APP_DEBUG: bool = Field(True, env='APP_DEBUG')
    APP_URL: str = Field('http://localhost:8000', env='APP_URL')
    APP_CORS_DOMAINS: str = Field(..., env='APP_CORS_DOMAINS')
    APP_TRUSTED_HOSTS: str = Field(..., env='APP_TRUSTED_HOSTS')

    STATICS_DIRECTORY: str = f'{PROJECT_DIR}/static'
    STATICS_ROUTE: str = '/static'
    STATICS_PATH: str = f'{PROJECT_PATH}/{STATICS_DIRECTORY}'

    ADMIN_TEMPLATE_PATH: str = f'{APP_PATH}/templates/admin'
    FRONT_TEMPLATE_PATH: str = f'{APP_PATH}/templates/front'

    DB_CONNECTION: str = Field(..., env='DB_CONNECTION')
    DB_HOST: str = Field('127.0.0.1', env='DB_HOST')
    DB_PORT: str = Field('', env='DB_PORT')
    DB_USER: str = Field('', env='DB_USER')
    DB_PASSWORD: str = Field('', env='DB_PASSWORD')
    DB_DATABASE: str = Field('', env='DB_DATABASE')
    DB_PREFIX: str = Field('', env='DB_PREFIX')

    MAIL_PROVIDER: str = Field('', env='MAIL_PROVIDER')
    MAIL_HOST: str = Field('', env='MAIL_HOST')
    MAIL_PORT: str = Field('', env='MAIL_PORT')
    MAIL_ENCRYPTION: str = Field(True, env='MAIL_ENCRYPTION')
    MAIL_USERNAME: str = Field('', env='MAIL_USERNAME')
    MAIL_PASSWORD: str = Field('', env='MAIL_PASSWORD')

    class Config:
        case_sensitive = True
        env_file = ENV_PATH
        env_file_encoding = 'utf-8'


appConfigs = AppConfigs()
appConfigs.APP_CORS_DOMAINS = appConfigs.APP_CORS_DOMAINS.split(',')
appConfigs.APP_TRUSTED_HOSTS = appConfigs.APP_TRUSTED_HOSTS.split(',')
print(appConfigs.dict())
