import unittest
from api.database import DBConn
from api.models import Models


class ModelsTest(unittest.TestCase):
    def test_connection(self):
        DBConn.reset()
        with self.assertRaises(TypeError):
            DBConn.Session()
        DBConn()
        with DBConn.get_session() as sess:
            self.assertTrue(sess)

    def test_models(self):
        models = Models()
        self.assertGreater(len(models.schemas), 0)

        list_ = list(models)
        self.assertGreater(len(list_), 0)

        models2 = Models()
        self.assertEqual(len(models.schemas), len(models2.schemas))
