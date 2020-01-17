import unittest
from collections import namedtuple

from api.config import Config
from api.erd import ERD, Algorithm
from api.system import Hierachy, HierachyConstructor

DummyRole = namedtuple('DummyRole', ['name'])


class TestHierarchy(unittest.TestCase):
    def setUp(self):
        config = Config()
        config.Models['models_dir'] = '_temp'
        with open('../xml/example.xml', 'r') as f:
            xml = f.read()
        erd = ERD(xml)
        alg = Algorithm(erd)
        alg.run_algorithm()

        self.alg = alg
        self.erd = erd

    def test_constructor(self):
        dummy_admin = DummyRole(name='admin')
        constructor = HierachyConstructor(self.alg.tables, 'er1', dummy_admin)

        hierarchy = constructor.construct()

        self.assertEqual(
            hierarchy.pretty_xml(),
            Hierachy.from_xml(hierarchy.pretty_xml()).pretty_xml()
        )

        self.assertDictEqual(
            hierarchy.to_object(),
            Hierachy.from_xml(hierarchy.pretty_xml()).to_object()
        )

    def test_extract(self):
        admin1 = DummyRole(name='admin1')
        admin2 = DummyRole(name='admin2')
        c1 = HierachyConstructor(self.alg.tables, 'er1', admin1)
        c2 = HierachyConstructor(self.alg.tables, 'er2', admin2)
        h1 = c1.construct()

        h = Hierachy.from_xml(h1.to_xml())
        h2 = c2.construct()

        h1.merge(h2)
        self.assertEqual(
            h1.pretty_xml(),
            Hierachy.from_xml(h1.pretty_xml()).pretty_xml()
        )

        h3 = h1.extract(admin1.name)
        self.assertEqual(
            h.pretty_xml(),
            h3.pretty_xml()
        )
