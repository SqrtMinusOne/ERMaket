from api.database import DBConn
from api.queries import QueryBuilder
from api.models import Models, Seeder, Faker

import unittest


class TestQueries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DBConn()
        models = Models()
        cls.MODEL = next(iter(models))
        cls.MODEL_NAME = cls.MODEL.__name__
        cls.FIELD_NAME = next(iter(cls.MODEL.__table__.columns)).name

        faker = Faker(models, verbose=True)
        seeder = Seeder(models)
        seeder.create_models()
        faker.fake_all(10)

    def _get_sample(self, db):
        q = db.query(self.MODEL).first()
        obj = q.__marshmallow__().dump(q)

        criterion = {
            "field_name": f"{self.MODEL_NAME}.{self.FIELD_NAME}",
            "operator": "==",
            "field_value": obj[self.FIELD_NAME]
        }
        return obj, criterion

    def test_fetch_many(self):
        with DBConn.get_session() as db:
            obj, criterion = self._get_sample(db)

            builder = QueryBuilder(db)
            result = builder.fetch_data(self.MODEL, filter_by=[criterion])
            self.assertGreater(len(result), 0)

    def test_fetch_one(self):
        with DBConn.get_session() as db:
            obj, criterion = self._get_sample(db)

            builder = QueryBuilder(db)
            found_obj = builder.fetch_one(self.MODEL, filter_by=[criterion])
            self.assertDictEqual(obj, found_obj)
