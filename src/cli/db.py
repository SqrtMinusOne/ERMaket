import click
import simplejson as json

from api.database import DBConn
from api.erd import ERD, Algorithm
from api.generation import Generator
from api.models import Faker, Models, Seeder


__all__ = ['db']


@click.group(help='Models management')
def db():
    pass


@db.command(help='Check connection & models')
def check():
    DBConn()
    Models()


@db.command(help='Drop data from database')
@click.option("--schema", help="Schema to drop")
def drop(schema):
    if click.confirm("Drop cannot be undone. Continue?"):
        DBConn()
        if schema:
            seeder = Seeder(None)
            seeder.drop_models(schema)
        else:
            models = Models()
            seeder = Seeder(models)
            seeder.drop_models(schema)


@db.command(help='Create table in the database')
def create():
    DBConn()
    models = Models()
    seeder = Seeder(models)
    seeder.create_models()


@db.command(help='Generate models by xml schema')
@click.option("--xml",
              prompt=True,
              help="XML file with schema",
              type=click.Path())
@click.option("--schema", prompt=True, help="Name of schema")
def generate(xml, schema):
    with open(xml, 'r') as f:
        xml = f.read()
    erd = ERD(xml)
    alg = Algorithm(erd)
    alg.run_algorithm()

    gen = Generator(alg.tables, schema)
    gen.generate_folder()

    click.echo(
        'Generation complete. Run --check to make sure everything is OK')


@db.command(help='Clear generated models')
@click.option("--folder", help="Folder to clear", type=click.Path())
@click.option("--schema", help="Schema to clear")
def clear(folder, schema):
    gen = Generator(None, None)
    gen.clear_folder(folder=folder, schema=schema)


@db.command(help='Fake data')
@click.option('--all',
              help='Create data in all schemas',
              default=False,
              is_flag=True)
@click.option('--schema', help='Create data only in given schema instead')
@click.option('--num',
              help='Default number of entries to be created',
              default=5)
@click.option('--config',
              help='JSON file with creation settings (only for schema)')
@click.option('--fake',
              help='Make human-readable data',
              default=False,
              is_flag=True)
@click.option('--refill',
              help='Drop & create tables before',
              default=False,
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