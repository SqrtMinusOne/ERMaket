from collections import namedtuple

import click

from api.erd import ERD, Algorithm
from api.system import HierachyConstructor, HierachyManager

DummyRole = namedtuple('DummyRole', ['name'])

__all__ = ['hierarchy']


@click.group(help='Hierachy Management')
def hierarchy():
    pass


@hierarchy.command(help='Generate hierarchy by xml schema')
@click.option(
    "--xml", prompt=True, help="XML file with schema", type=click.Path()
)
@click.option("--schema", prompt=True, help="Name of schema")
@click.option("--admin", help="Admin role name")
def generate(xml, schema, admin):
    with open(xml, 'r') as f:
        xml = f.read()
    erd = ERD(xml)
    alg = Algorithm(erd)
    alg.run_algorithm()

    role = None
    if admin:
        role = DummyRole(admin)
    constructor = HierachyConstructor(alg.tables, schema, role)
    hierarchy = constructor.construct()

    manager = HierachyManager()
    manager.hierarchy.merge(hierarchy)


@hierarchy.command(help='Drop hierarchy')
@click.option(
    "--schema", help="Name of schema. If not mentioned, will drop all"
)
def drop(schema):
    manager = HierachyManager()
    if schema:
        manager.hierarchy.drop_schema(schema)
    else:
        manager.drop()
