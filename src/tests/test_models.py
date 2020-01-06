import unittest

from api.config import Config
from api.database import DBConn
from api.models import Models


class ModelsTest(unittest.TestCase):
    def setUp(self):
        Config(reload=True)

    def test_connection(self):
        DBConn.reset()
        with self.assertRaises(TypeError):
            DBConn.Session()
        DBConn()
        with DBConn.get_session() as sess:
            self.assertTrue(sess)

    def test_models(self):
        DBConn()
        models = Models()
        self.assertGreater(len(models.schemas), 0)

        list_ = list(models)
        self.assertGreater(len(list_), 0)

        models2 = Models()
        self.assertEqual(len(models.schemas), len(models2.schemas))

    def test_marshmallow(self):
        DBConn()
        models = Models()
        for model in iter(models):
            self.assertTrue(hasattr(model, '__marshmallow__'))
