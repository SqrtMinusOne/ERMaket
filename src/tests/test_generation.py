import unittest
from api.erd import ERD, Algorithm
from api.generation import Generator


class TestGeneration(unittest.TestCase):
    def test_templating(self):
        with open('../xml/example.xml', 'r') as f:
            xml = f.read()
        erd = ERD(xml)
        alg = Algorithm(erd)
        alg.run_algorithm()
        tables = alg.tables

        gen = Generator(tables, 'er1')
        gen.generate_models('_temp')
