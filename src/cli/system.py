import click

from api.system import UserManager

__all__ = ['system']


@click.group(help='System management')
def system():
    pass


@system.command(help='Add user')
@click.option("--login", prompt=True)
@click.option(
    "--password", prompt=True, hide_input=True, confirmation_prompt=True
)
@click.option("--role", multiple=True)
def useradd(login, password, role):
    UserManager().add_user(login, password, role_names=role)
