import unittest

from bs4 import BeautifulSoup

from api.erd import ERD, Algorithm


class TestAlgorithm(unittest.TestCase):
    def setUp(self):
        with open('../xml/example.xml', 'r') as f:
            self.xml = f.read()
        self.soup = BeautifulSoup(self.xml, 'xml')

    def test_is_works(self):
        erd = ERD(self.xml)
        algorithm = Algorithm(erd)
        algorithm.run_algorithm()
        print(algorithm)
