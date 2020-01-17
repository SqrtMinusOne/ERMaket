import pytest

from api.erd import ERD, Algorithm
from api.erd.er_entities import Relation

from .dummies import DummyEntity, binary_erd, non_binary_erds


class ERDTest(ERD):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successful_iters = 0

    def iter_relations(self, *args, **kwargs):
        ret = list(super().iter_relations(*args, **kwargs))
        if len(ret) > 0:
            self.successful_iters += 1
        return ret


@pytest.mark.usefixtures("sample_xml")
def test_examlple(sample_xml):
    erd = ERD(sample_xml)
    algorithm = Algorithm(erd)
    algorithm.run_algorithm()
    # print(algorithm.tables)


def test_merge():
    erd = ERD()
    erd.add_entity(DummyEntity(0))
    erd.add_entity(DummyEntity(1))
    erd.add_entity(DummyEntity(2))
    erd.add_relation(Relation.make('m0', [0, True, False], [1, True, False]))
    erd.add_relation(Relation.make('m1', [1, True, False], [2, True, False]))

    alg = Algorithm(erd)
    alg.run_algorithm()
    assert len(alg.tables) == 1
    # print(alg)


def test_binary():
    erds = binary_erd()
    for erd in erds:
        test_erd = ERDTest(str(erd.to_xml()))
        alg = Algorithm(test_erd)
        alg.run_algorithm()
        assert len(alg.tables) > 0
        assert test_erd.successful_iters == 1


def test_non_binary():
    for erd in non_binary_erds(range(3, 10)):
        alg = Algorithm(erd)
        alg.run_algorithm()
        assert len(alg.tables) > 0
