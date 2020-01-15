import unittest

import numpy as np

from api.erd import ERD, Algorithm
from api.erd.er_entities import Relation

from .dummies import DummyEntity, binary_erd, non_binary_erds


class TestingERD(ERD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successful_iters = 0

    def iter_relations(self, *args, **kwargs):
        ret = list(super().iter_relations(*args, **kwargs))
        if len(ret) > 0:
            self.successful_iters += 1
        return ret


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        np.random.seed(42)

    def test_examlple(self):
        with open('../xml/example.xml', 'r') as f:
            xml = f.read()
        erd = ERD(xml)
        algorithm = Algorithm(erd)
        algorithm.run_algorithm()
        # print(algorithm.tables)

    def test_merge(self):
        erd = ERD()
        erd.add_entity(DummyEntity(0))
        erd.add_entity(DummyEntity(1))
        erd.add_entity(DummyEntity(2))
        erd.add_relation(
            Relation.make('m0', [0, True, False], [1, True, False])
        )
        erd.add_relation(
            Relation.make('m1', [1, True, False], [2, True, False])
        )

        alg = Algorithm(erd)
        alg.run_algorithm()
        self.assertEqual(len(alg.tables), 1)
        # print(alg)

    def test_binary(self):
        erds = binary_erd()
        for erd in erds:
            test_erd = TestingERD(str(erd.to_xml()))
            alg = Algorithm(test_erd)
            alg.run_algorithm()
            self.assertGreater(len(alg.tables), 0)
            self.assertEqual(test_erd.successful_iters, 1)

    def test_non_binary(self):
        for erd in non_binary_erds(range(3, 10)):
            alg = Algorithm(erd)
            alg.run_algorithm()
            self.assertGreater(len(alg.tables), 0)
