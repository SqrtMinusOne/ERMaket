import unittest
import numpy as np

from api.erd import ERD, Algorithm
from api.erd.er_entities import Relation


from .dummies import binary_erd, non_binary_erds, DummyEntity


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
            Relation.make('m0', [0, True, False], [1, True, False]))
        erd.add_relation(
            Relation.make('m1', [1, True, False], [2, True, False]))

        alg = Algorithm(erd)
        alg.run_algorithm()
        self.assertEqual(len(alg.tables), 1)
        # print(alg)

    def test_binary(self):
        erd = binary_erd()
        alg = Algorithm(erd)
        alg.run_algorithm()

    def test_non_binary(self):
        for erd in non_binary_erds(range(3, 10)):
            alg = Algorithm(erd)
            alg.run_algorithm()
            self.assertGreater(len(alg.tables), 0)
