import pytest

from api.database import DBConn
from api.erd import ERD, Algorithm
from api.generation import Generator
from api.models import Faker, Seeder

from .dummies import binary_erd


@pytest.mark.usefixtures("config", "sample_xml", "models")
def test_integration(config, sample_xml, models):
    config.Models['models_dir'] = '_temp'
    erd = ERD(sample_xml)
    alg = Algorithm(erd)
    alg.run_algorithm()
    alg.inject_role_ref(0)
    tables = alg.tables

    gen = Generator(tables, 'er1')
    gen.generate_folder('_temp')
    gen.generate_system_models('_temp')

    assert len(list(models)) - len(models['system']) == len(tables)

    seeder = Seeder(models)
    seeder.drop_models()
    seeder.create_models()

    faker = Faker(models)
    faker.fake_all(10)
    with DBConn.get_session() as db:
        for table in iter(models):
            assert db.query(table).first()

    assert repr(erd)
    assert repr(alg)
    assert repr(gen)


def test_dummies():
    erds = binary_erd()
    for i, erd in enumerate(erds):
        alg = Algorithm(erd)
        alg.run_algorithm()
        gen = Generator(alg.tables, 'er1')
        models_ = gen.generate_models()
        assert len(models_) > 0
