import numpy as np

from api.erd import ERD
from api.erd.er_entities import Entity, Relation

__all__ = ['DummyEntity', 'binary_erd', 'non_binary_erds']


class DummyEntity(Entity):
    def __init__(self, _id):
        super().__init__(_id, name=f"entity_{_id}", attributes=[])


def binary_erd():
    erd = ERD()
    for i in range(16):
        params = bin(i)[2:].zfill(4)
        a1, a2, b1, b2 = [a == "1" for a in params]
        erd.add_entity(DummyEntity(i * 2))
        erd.add_entity(DummyEntity(i * 2 + 1))
        name = params.replace('0', 'A').replace('1', 'B')
        erd.add_relation(
            Relation.make(name, [i * 2, a1, a2], [i * 2 + 1, b1, b2]))
    return erd


def non_binary_erds(n_iter):
    for n in n_iter:
        erd = ERD()
        [erd.add_entity(DummyEntity(i)) for i in range(n)]
        erd.add_relation(
            Relation.make('relation', *[[i, *(np.random.rand(2) > 0.5)]
                                        for i in range(n)]))
        yield erd
