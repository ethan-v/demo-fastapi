import click


@click.command(help='Build project')
@click.option('--docker', is_flag=True, help='Indicates the project should be built into docker image')
def build(docker):
    if docker:
        print('Building this repo into a docker image...')
    else:
        print('Building this repo using default method...')
