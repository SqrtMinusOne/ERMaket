import numpy as np
import pytest

from utils import Singleton

_created = 0


class Dummy(metaclass=Singleton):
    def __init__(self):
        global _created
        _created += 1
        self.info = np.random.random()


def test_create():
    global _created

    _created = 0
    a = Dummy()
    b = Dummy()
    c = Dummy()

    assert _created == 1
    assert a.info == b.info == c.info


def test_reset():
    global _created
    Singleton.reset()
    _created = 0
    a = Dummy()
    b = Dummy()
    Singleton.reset()
    c = Dummy()

    assert _created == 2
    assert a.info == b.info
    assert a.info != c.info


@pytest.mark.usefixtures('block_singletons')
def test_block():
    global _created

    _created = 0
    a = Dummy()
    b = Dummy()
    c = Dummy()

    assert _created == 3
    assert a.info != b.info != c.info
