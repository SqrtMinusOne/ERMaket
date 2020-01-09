import unittest

from api.database import DBConn
from api.system import SystemManager, UserManager


class TestAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        DBConn()
        SystemManager().drop_system_tables()
        SystemManager().create_system_tables()

    def test_create(self):
        manager = UserManager()
        self.assertIsNone(manager.check_user('admin', 'password'))
        manager.add_user('admin', 'password')
        self.assertIsNotNone(manager.check_user('admin', 'password'))
        self.assertIsNone(manager.check_user('admin', 'password1'))
        self.assertIsNone(manager.check_user('admin1', 'password'))
