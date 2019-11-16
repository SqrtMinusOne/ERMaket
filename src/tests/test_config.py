import unittest

from api import Config


class ConfigTest(unittest.TestCase):
    def test_config(self):
        config = Config()
        self.assertTrue(hasattr(config, 'Database'))
