import logging

import click

from api.config import Config
from cli import db, system


@click.group()
@click.option('--log', default=False, is_flag=True)
def cli(log):
    if log:
        logger = logging.getLogger('sqlalchemy.engine')
        logger.setLevel(logging.INFO)

        config = Config()
        logging.basicConfig(
            level=logging.DEBUG,
            format=config.Logging['formatters']['single-line']['format'],
            datefmt='%I:%M:%S')


cli.add_command(db)
cli.add_command(system)
if __name__ == "__main__":
    cli()
