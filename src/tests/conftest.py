import numpy as np
import pytest

from api.config import Config
from api.database import DBConn
from api.erd import ERD, Algorithm
from api.models import Models


@pytest.fixture()
def sample_xml():
    with open('../xml/example.xml', 'r') as f:
        yield f.read()


@pytest.fixture()
def config():
    config = Config(reload=True)
    return config


@pytest.fixture()
def models():
    DBConn()
    return Models()


@pytest.fixture()
def temp_models_dir(config):
    config.Models['models_dir'] = '_temp'


@pytest.fixture()
def sample_erd(config, sample_xml):
    erd = ERD(sample_xml)
    return erd


@pytest.fixture()
def algorithm(sample_erd):
    alg = Algorithm(sample_erd)
    alg.run_algorithm()
    return alg


@pytest.fixture()
def randomize(autouse=True):
    np.random.seed(42)
