from api.database import DBConn
from api.models import Models, Seeder, Faker

import click
import logging
import simplejson as json


@click.group()
@click.option('--log', default=False, is_flag=True)
def cli(log):
    if log:
        logger = logging.getLogger('sqlalchemy.engine')
        logger.setLevel(logging.INFO)


@cli.command(help='Check connection & models')
def check():
    DBConn()
    Models()


@cli.command(help='Drop data from database')
@click.option("--schema", help="Schema to drop")
def drop(schema):
    if click.confirm("Drop cannot be undone. Continue?"):
        DBConn()
        models = Models()
        seeder = Seeder(models)
        seeder.drop_models(schema)


@cli.command(help='Create table in the database')
def create():
    DBConn()
    models = Models()
    seeder = Seeder(models)
    seeder.create_models()


@cli.command(help='Fake data')
@click.option('--all', help='Create data in all schemas', default=False,
              is_flag=True)
@click.option('--schema', help='Create data only in given schema instead')
@click.option('--num', help='Default number of entries to be created',
              default=5)
@click.option('--config',
              help='JSON file with creation settings (only for schema)')
@click.option('--fake', help='Make human-readable data', default=False,
              is_flag=True)
@click.option('--refill', help='Drop & create tables before', default=False,
              is_flag=True)
def fake(all, schema, num, config, fake, refill):
    DBConn()
    models = Models()
    if refill:
        seeder = Seeder(models)
        seeder.drop_models(schema)
        seeder.create_models()
    faker = Faker(models, verbose=True, fake=fake)
    if all:
        faker.fake_all(num)
    elif schema:
        entries = {}
        if config:
            with open(config, 'r') as f:
                entries = json.load(f)
        faker.fake_schema(schema, entries, num)
    else:
        click.echo('Set either --all or --schema <schema name>')


if __name__ == "__main__":
    cli()
