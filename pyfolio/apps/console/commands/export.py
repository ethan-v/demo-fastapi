import click

from pyfolio.apps.console.openapi import generate_openapi


@click.command(help='Export openapi.json, ..etc')
@click.argument('export_name')
def export(export_name):
    """
    Usage: pyfolio export openapi
    """
    if export_name == 'openapi':
        generate_openapi()
        print('Export API to Openapi.json...')
    else:
        print('Please input export name method...')
