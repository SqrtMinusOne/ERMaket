import unittest

from bs4 import BeautifulSoup

from api.erd.er_entities import Entity, Relation, XMLObject
from api.erd import ERD


class TestXML(unittest.TestCase):
    def setUp(self):
        with open('../xml/example.xml', 'r') as f:
            self.xml = f.read()
        self.soup = BeautifulSoup(self.xml, 'xml')
        XMLObject.soup = self.soup

    def test_conv(self):
        entities = [
            Entity.from_xml(tag) for tag in self.soup.find_all('entity')
        ]
        relations = [
            Relation.from_xml(tag) for tag in self.soup.find_all('relation')
        ]
        self.assertGreater(len(entities), 0)
        self.assertGreater(len(relations), 0)

    def test_invariant(self):
        entities_tags = list(self.soup.find_all('entity'))
        rel_tags = list(self.soup.find_all('relation'))
        [
            self.assertEqual(
                Entity.from_xml(tag).to_xml().prettify(),
                tag.prettify()[:-1]) for tag in entities_tags
        ]
        [
            self.assertEqual(
                Relation.from_xml(tag).to_xml().prettify(),
                tag.prettify()[:-1]) for tag in rel_tags
        ]

    def test_ERD(self):
        erd = ERD(self.xml)
        self.assertGreater(len(erd.entities), 0)
