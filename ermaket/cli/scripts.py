import click

from ermaket.api.scripts import ScriptManager

__all__ = ['scripts']


@click.group(help='Script Management')
def scripts():
    pass


@scripts.command(help='Automatically generate the script config file')
def discover():
    ScriptManager(discover=True)
