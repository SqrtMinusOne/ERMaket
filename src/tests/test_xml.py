import unittest

from bs4 import BeautifulSoup

from api.config import Config
from api.erd import ERD
from api.erd.er_entities import Entity, Relation, XMLObject
from api.system.hierarchy_entities import xmllist, xmltuple


class TestXML(unittest.TestCase):
    def setUp(self):
        Config(reload=True)
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
                tag.prettify()[:-1]
            ) for tag in entities_tags
        ]
        [
            self.assertEqual(
                Relation.from_xml(tag).to_xml().prettify(),
                tag.prettify()[:-1]
            ) for tag in rel_tags
        ]

    def test_ERD(self):
        erd = ERD(self.xml)
        new_xml = erd.to_xml()
        self.assertEqual(self.soup.prettify(), new_xml.prettify())

    def test_tuple(self):
        Tag = xmltuple('Tag', 'tag', ['a', 'b'])
        tag = Tag(1, 2)
        tag2 = Tag(a=1, b=2)
        self.assertEqual(tag.a, 1)
        self.assertEqual(tag2.b, 2)
        self.assertEqual(tag.to_xml(), tag2.to_xml())

        self.assertEqual(tag.to_xml(), Tag.from_xml(tag.to_xml()).to_xml())

        Tag2 = xmltuple('Tag2', 'tag2', ['id', 'boo', 'far'], kws=['id'])
        tag2 = Tag2(1, 2, 3)
        self.assertEqual(tag2.to_xml(), Tag2.from_xml(tag2.to_xml()).to_xml())

    def test_nested_tuple(self):
        Tag1 = xmltuple('Tag1', 'tag1', ['foo', 'bar'])
        Tag2 = xmltuple('Tag2', 'tag2', ['boo'])
        Tag = xmltuple(
            'Tag', 'tag', ['tag1', 'tag2'], {
                'tag1': Tag1,
                'tag2': Tag2
            }
        )
        tag = Tag(tag1=Tag1(foo='a', bar='b'), tag2=Tag2(boo='c'))
        self.assertEqual(tag.to_xml(), Tag.from_xml(tag.to_xml()).to_xml())

    def test_list(self):
        Tag = xmltuple('Tag', 'tag', ['foo', 'bar'])
        List = xmllist('List', 'list', Tag)
        list_ = List([Tag(1, 2), Tag(3, 4), Tag(5, 6)])
        self.assertEqual(
            list_.to_xml(),
            List.from_xml(list_.to_xml()).to_xml()
        )

        List2 = xmllist('List2', 'list2', 'tag')
        list2 = List2([1, 2, 3, 4])
        self.assertEqual(
            list2.to_xml(),
            List2.from_xml(list2.to_xml()).to_xml()
        )

        List3 = xmllist('List3', 'list3', 'tag', ['id', 'foo'])
        list3 = List3([6, 66], 4, 'bar')
        self.assertEqual(
            list3.to_xml(),
            List3.from_xml(list3.to_xml()).to_xml()
        )
