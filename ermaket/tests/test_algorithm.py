import pytest

from ermaket.api.erd import ERD, Algorithm
from ermaket.api.erd.er_entities import Relation

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


TEST_OPTIONS = {
    "respect_n_obligation": True,
}


def check_sanity(alg: Algorithm):
    for table in alg.tables.values():
        assert table.pk is not None
        for fk_col in table.foreign_keys:
            assert fk_col.fk.column is not None
        for relationship in table.relationships:
            assert relationship.ref_rel is not None


@pytest.mark.usefixtures("sample_xml")
def test_example(sample_xml):
    erd = ERD(sample_xml)
    algorithm = Algorithm(erd, options=TEST_OPTIONS)
    algorithm.run_algorithm()
    check_sanity(algorithm)


def test_merge():
    erd = ERD()
    erd.add_entity(DummyEntity(0))
    erd.add_entity(DummyEntity(1))
    erd.add_entity(DummyEntity(2))
    erd.add_relation(Relation.make('m0', [0, True, False], [1, True, False]))
    erd.add_relation(Relation.make('m1', [1, True, False], [2, True, False]))

    alg = Algorithm(erd, options=TEST_OPTIONS)
    alg.run_algorithm()
    check_sanity(alg)
    assert len(alg.tables) == 1
    # print(alg)


def test_binary():
    erds = binary_erd()
    for erd in erds:
        test_erd = ERDTest(str(erd.to_xml()))
        alg = Algorithm(test_erd, options=TEST_OPTIONS)
        alg.run_algorithm()
        # print('==================================================')
        # print(test_erd)
        # print('====================')
        # print(alg.tables)
        # print('==================================================')
        assert len(alg.tables) > 0
        assert test_erd.successful_iters == 1
        check_sanity(alg)


def test_non_binary():
    for erd in non_binary_erds(range(3, 10)):
        alg = Algorithm(erd, options=TEST_OPTIONS)
        alg.run_algorithm()
        assert len(alg.tables) > 0
        check_sanity(alg)
