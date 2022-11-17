import click
from .commands import build, export, db


# Top level: pyfolio --help
@click.group(help="CLI tool to manage full development cycle of projects")
def cli():
    pass


# Group db: pyfolio db --help
@cli.group("db")
def cli_db():
    """Working with database"""


# pyfolio build --help
cli.add_command(build.build)
cli.add_command(export.export)

# Second level: db
cli_db.add_command(db.import_from_file)

def main():
    cli()


if __name__ == '__main__':
    main()
