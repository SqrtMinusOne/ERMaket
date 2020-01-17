from pathlib import Path
import numpy as np
import pytest
import shutil

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
def temp_paths(config):
    shutil.rmtree('_temp', ignore_errors=True)
    Path('_temp/xml').mkdir(parents=True, exist_ok=True)
    config.Models['models_dir'] = '_temp'
    config.XML['hierarchyPath'] = '_temp/xml/hierarchy.xml'


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
