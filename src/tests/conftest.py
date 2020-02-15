import os
import shutil
from collections import namedtuple
from pathlib import Path

import numpy as np
import pytest
from deepmerge import always_merger

from api.config import Config
from api.database import DBConn
from api.erd import ERD, Algorithm
from api.generation import Generator
from api.models import Faker, Models, Seeder
from api.system import HierachyConstructor, HierachyManager, UserManager
from app import create_app

SAMPLE_ERD = '../xml/example.xml'


@pytest.fixture()
def sample_xml():
    with open(SAMPLE_ERD, 'r') as f:
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
def alg_test_options():
    return {
        "respect_n_obligation": True,
    }


@pytest.fixture()
def randomize(autouse=True):
    np.random.seed(42)


@pytest.fixture(scope='module')
def empty_db():
    config = Config(reload=True)

    with open(SAMPLE_ERD, 'r') as f:
        xml = f.read()
    erd = ERD(xml)
    alg = Algorithm(erd)
    alg.run_algorithm()

    shutil.rmtree('_temp', ignore_errors=True)
    Path('_temp/xml').mkdir(parents=True, exist_ok=True)
    config.Models['models_dir'] = '_temp'
    config.XML['hierarchyPath'] = '_temp/xml/hierarchy.xml'

    alg.inject_role_ref(0)

    gen = Generator(alg.tables, 'er1')
    gen.generate_folder()
    gen.generate_system_models()

    models = Models()

    seeder = Seeder(models)
    seeder.drop_models()
    seeder.create_models()
    return alg, models


@pytest.fixture(scope='module')
def test_db(empty_db):
    alg, models = empty_db
    manager = UserManager()
    hierarchy_manager = HierachyManager()
    hierarchy_manager.drop()

    with DBConn.get_session() as db:
        admin_user = manager.add_user('admin', 'password', db)
        normal_user = manager.add_user('user', 'password', db)
        admin_role = models['system']['Role'](
            name='admin', can_reset_password=True, has_sql_access=True
        )
        db.add(admin_role)
        admin_user.roles = [admin_role]
        db.commit()

        hierarchy_manager.h.merge(
            HierachyConstructor(alg.tables, 'er1',
                                admin_role=admin_role).construct()
        )

    faker = Faker(models)
    faker.fake_all(5)

    model = next(iter(models))
    model_name = model.__name__
    field_name = next(iter(model.__table__.columns)).name

    User = namedtuple('User', ['user', 'login', 'password'])
    admin = User(admin_user, 'admin', 'password')
    normal = User(normal_user, 'user', 'password')

    TestData = namedtuple(
        'TestData', [
            'admin_user', 'normal_user', 'model', 'model_name', 'field_name',
            'schema'
        ]
    )
    return TestData(
        admin_user=admin,
        normal_user=normal,
        model=model,
        model_name=model_name,
        field_name=field_name,
        schema='er1'
    )


@pytest.fixture(scope='module')
def client(test_db, clear_test_logs):
    config = Config()
    config.configs['Logging'] = always_merger.merge(
        config.Logging, config.TestingLogging
    )
    config.configs['Logging']['root']['handlers'] = [
        "file_handler", "error_file_handler"
    ]
    flask_app = create_app()
    flask_app.config.update(config.TestingFlask)
    client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()

    yield client
    ctx.pop()


@pytest.fixture(scope='session')
def clear_test_logs():
    config = Config()
    try:
        os.remove(
            config.TestingLogging['handlers']['file_handler']['filename']
        )
    except OSError:
        pass
    try:
        os.remove(
            config.TestingLogging['handlers']['error_file_handler']['filename']
        )
    except OSError:
        pass
