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
        alg.inject_role_ref(0)
        tables = alg.tables

        gen = Generator(tables, 'er1')
        gen.generate_folder('_temp')
        gen.generate_system_models('_temp')

        DBConn()
        models = Models()
        self.assertEqual(
            len(list(models)) - len(models['system']), len(tables)
        )

        seeder = Seeder(models)
        seeder.drop_models()
        seeder.create_models()

        faker = Faker(models)
        faker.fake_all(10)
        with DBConn.get_session() as db:
            for table in iter(models):
                self.assertTrue(db.query(table).first())

        self.assertIsNotNone(repr(erd))
        self.assertIsNotNone(repr(alg))
        self.assertIsNotNone(repr(gen))

    def test_dummies(self):
        erds = binary_erd()
        for i, erd in enumerate(erds):
            alg = Algorithm(erd)
            alg.run_algorithm()
            gen = Generator(alg.tables, 'er1')
            models = gen.generate_models()
            self.assertGreater(len(models), 0)
