import difflib
import sys
from collections import namedtuple

import click

from api.erd import ERD, Algorithm
from api.system import HierachyConstructor, HierachyManager
from api.system.hierarchy import Hierachy

DummyRole = namedtuple('DummyRole', ['name'])

__all__ = ['hierarchy']


@click.group(help='Hierachy Management')
def hierarchy():
    pass


@hierarchy.command(help='Generate the hierarchy by xml schema')
@click.option(
    "--xml", prompt=True, help="XML file with schema", type=click.Path()
)
@click.option("--schema", prompt=True, help="Name of schema")
@click.option("--admin", help="Admin role name")
@click.option(
    '--system', is_flag=True, default=False, help="Insert system pages"
)
@click.option(
    "--path", default=None, type=click.Path(), help="Path to save hierarchy"
)
def generate(xml, schema, admin, system, path):
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
    if system:
        constructor.insert_system_pages(hierarchy)

    manager = HierachyManager(path=path)
    manager.hierarchy.merge(hierarchy)


@hierarchy.command(help='Merge target hierarchy into the source one')
@click.option("--target", type=click.Path(), prompt=True)
@click.option("--source", type=click.Path(), default=None)
def merge(target, source):
    with open(target, 'r') as f:
        xml = f.read()
    hierarchy = Hierachy.from_xml(xml)
    manager = HierachyManager(path=source)
    manager.h.merge(hierarchy)


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


@hierarchy.command(help='Check if the hierarchy is correct')
@click.option("--xml", help="Path to the hierarchy file", type=click.Path())
def check(xml):
    with open(xml, 'r') as f:
        xml = f.read()
    xml1 = Hierachy.from_xml(xml).pretty_xml()
    xml2 = Hierachy.from_xml(xml1).pretty_xml()

    check = xml1 == xml2
    if check:
        click.echo('Everyting seems to be correct')
    else:
        click.echo(
            'Something is wrong. Perhaps the following can help', err=True
        )
        sys.stdout.writelines(
            difflib.unified_diff(xml1.splitlines(), xml2.splitlines())
        )
