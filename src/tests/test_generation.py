import unittest

from api.config import Config
from api.database import DBConn
from api.erd import ERD, Algorithm
from api.generation import Generator
from api.models import Faker, Models, Seeder

from .dummies import binary_erd


class TestGeneration(unittest.TestCase):
    def setUp(self):
        Config(reload=True)

    def test_integration(self):
        config = Config()
        config.Models['models_dir'] = '_temp'
        with open('../xml/example.xml', 'r') as f:
            xml = f.read()
        erd = ERD(xml)
        alg = Algorithm(erd)
        alg.run_algorithm()
        tables = alg.tables

        gen = Generator(tables, 'er1')
        gen.generate_folder('_temp')

        DBConn()
        models = Models()
        self.assertEqual(len(list(models)), len(tables))

        seeder = Seeder(models)
        seeder.drop_models()
        seeder.create_models()

        faker = Faker(models)
        faker.fake_all(10)
        with DBConn.get_session() as db:
            for table in iter(models):
                self.assertTrue(db.query(table).first())

    def test_dummies(self):
        erd = binary_erd()
        alg = Algorithm(erd)
        alg.run_algorithm()
        gen = Generator(alg.tables, 'er1')
        models = gen.generate_models()
        self.assertGreater(len(models), 0)
