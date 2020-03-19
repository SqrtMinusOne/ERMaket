import click
import simplejson as json

from api.database import DBConn
from api.erd import ERD, Algorithm
from api.generation import Generator
from api.models import Dumper, Faker, Models, Seeder

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
@click.option("-y", help="skip warning", default=False, is_flag=True)
def drop(schema, y):
    if not y:
        if not click.confirm("Drop cannot be undone. Continue?"):
            return
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
@click.option(
    "--xml", prompt=True, help="XML file with schema", type=click.Path()
)
@click.option("--schema", prompt=True, help="Name of schema")
@click.option(
    "--no-system",
    default=False,
    is_flag=True,
    help='Do not generate system tables'
)
@click.option(
    "--folder",
    help="Folder where to put the generated classes",
    type=click.Path()
)
@click.option(
    "--check",
    help="Add methods to check mandatory relationships",
    is_flag=True,
    default=False
)
@click.option(
    "--prefix",
    help="Prefix for the generated files",
    default="model_"
)
@click.option(
    "--base-module",
    help="Base module import path. There has to be only one base.",
    default="models.base"
)
@click.option(
    "--base-folder",
    help="Base module location folder",
    default="models"
)
def generate(
    xml,
    schema,
    no_system,
    folder,
    check,
    prefix,
    base_module,
    base_folder
):
    with open(xml, 'r') as f:
        xml = f.read()
    erd = ERD(xml)
    alg = Algorithm(erd)
    alg.run_algorithm()

    gen = Generator(
        alg.tables,
        schema,
        folder=folder,
        prefix=prefix,
        add_check=check,
        base_module=base_module,
        base_folder=base_folder
    )
    gen.generate_folder()
    if not no_system:
        gen.generate_system_models()

    click.echo('Generation complete. Run check to make sure everything is OK')


@db.command(help='Clear generated models')
@click.option("--folder", help="Folder to clear", type=click.Path())
@click.option("--schema", help="Schema to clear")
def clear(folder, schema):
    gen = Generator(None, folder=folder)
    gen.clear_folder(schema=schema)


@db.command(help='Dump data')
@click.option("--folder", help="Folder to dump", default=None)
@click.option("--schema", help="Schema to dump", prompt=True)
@click.option("--format", help="Format", default='csv')
def dump(folder, schema, format):
    dumper = Dumper()
    dumper.dump_schema(folder=folder, schema=schema, format=format)


@db.command(help="Load data from the dump")
@click.option("--folder", help="Folder with dumps", default=None)
@click.option("--schema", help="Schema with dumps", prompt=True)
@click.option("--format", help="Format", default='csv')
def load(folder, schema, format):
    dumper = Dumper()
    dumper.load_schema(folder=folder, schema=schema, format=format)


@db.command(help='Fake data')
@click.option(
    '--all', help='Create data in all schemas', default=False, is_flag=True
)
@click.option('--schema', help='Create data only in given schema instead')
@click.option(
    '--num', help='Default number of entries to be created', default=5
)
@click.option(
    '--config', help='JSON file with creation settings (only for schema)'
)
@click.option(
    '--fake', help='Make human-readable data', default=False, is_flag=True
)
@click.option(
    '--refill',
    help='Drop & create tables before',
    default=False,
    is_flag=True
)
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
