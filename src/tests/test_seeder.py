import unittest

from api.config import Config
from api.database import DBConn
from api.models import Faker, Models, Seeder


class TestSeeder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Config(reload=True)
        DBConn()

    def test_seeder(self):
        models = Models()
        seeder = Seeder(models)
        seeder.drop_models()
        seeder.drop_models()
        seeder.create_models()
        seeder.drop_models()
        seeder.drop_models()

    def test_faker(self):
        models = Models()
        seeder = Seeder(models)
        faker = Faker(models)
        seeder.drop_models()
        seeder.create_models()
        faker.fake_all(10)
        assertions = []
        with DBConn.get_session() as db:
            for model in faker.faked_models():
                ok = db.query(model).first() is not None
                assertions.append(ok)
        [self.assertTrue(ok) for ok in assertions]
