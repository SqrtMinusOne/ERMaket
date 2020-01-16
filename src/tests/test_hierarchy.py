import unittest
from collections import namedtuple

from api.config import Config
from api.erd import ERD, Algorithm
from api.system import Hierachy, HierachyConstructor

DummyRole = namedtuple('DummyRole', ['name'])


class TestHierarchy(unittest.TestCase):
    def test_constructor(self):
        config = Config()
        config.Models['models_dir'] = '_temp'
        with open('../xml/example.xml', 'r') as f:
            xml = f.read()
        erd = ERD(xml)
        alg = Algorithm(erd)
        alg.run_algorithm()

        dummy_admin = DummyRole(name='admin')
        constructor = HierachyConstructor(alg.tables, 'er1', dummy_admin)

        hierarchy = constructor.construct()

        self.assertEqual(
            hierarchy.pretty_xml(),
            Hierachy.from_xml(hierarchy.pretty_xml()).pretty_xml()
        )
