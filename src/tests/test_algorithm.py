import unittest
import numpy as np

from bs4 import BeautifulSoup

from api.erd import ERD, Algorithm
from api.erd.er_entities import Entity, Relation


class DummyEntity(Entity):
    def __init__(self, _id):
        super().__init__(_id, name=f"entity_{_id}", attributes=[])


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        with open('../xml/example.xml', 'r') as f:
            self.xml = f.read()
        self.soup = BeautifulSoup(self.xml, 'xml')
        np.random.seed(42)

    def test_is_works(self):
        erd = ERD(self.xml)
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
        erd = ERD()
        for i in range(16):
            params = bin(i)[2:].zfill(4)
            a1, a2, b1, b2 = [a == "1" for a in params]
            erd.add_entity(DummyEntity(i * 2))
            erd.add_entity(DummyEntity(i * 2 + 1))
            erd.add_relation(
                Relation.make(params, [i * 2, a1, a2], [i * 2 + 1, b1, b2]))
        alg = Algorithm(erd)
        alg.run_algorithm()

    def test_non_binary(self):
        for n in range(3, 10):
            erd = ERD()
            [erd.add_entity(DummyEntity(i)) for i in range(n)]
            erd.add_relation(Relation.make(
                'relation',
                *[[i, *(np.random.rand(2) > 0.5)] for i in range(n)]
            ))
            alg = Algorithm(erd)
            alg.run_algorithm()
            self.assertGreater(len(alg.tables), 0)
