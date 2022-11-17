import os

import click

from pyfolio.apps.console.helpers.database import DBCliHelper
from pyfolio.configs.app import appConfigs


@click.command('import')
@click.option('--file', required=True, type=str, help='Example: --file=example/settings.json')
@click.option('--refresh', required=False, type=bool, default=False, help='Delete all current data and import')
def import_from_file(file: str, refresh: bool = False):
    """
    Import data from file *.json \n
    Example: pyfolio db import --file=example/settings.json
    """
    absolute_path = f'{appConfigs.APP_PATH}/{file}'
    DBCliHelper().import_from_json(file_path=absolute_path)
    print(f'pyfolio db import --file={file} --refresh={refresh}')
    print(f'Success import data from {file}')
