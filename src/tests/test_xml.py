import unittest

from bs4 import BeautifulSoup

from api.config import Config
from api.erd import ERD
from api.erd.er_entities import Entity, Relation, XMLObject
from api.system.hierarchy import xmlall, xmlenum, xmllist, xmltuple

from utils import defaultify_init


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

        TagA = xmltuple('TagA', 'tagA', ['a'], kws=['id'])
        tagA = TagA(a=1, id=2)
        self.assertEqual(tagA.to_xml(), TagA.from_xml(tagA.to_xml()).to_xml())

    def test_default(self):
        Tag = xmltuple('Tag', 'tag', ['a', 'b'])
        tag = Tag()
        self.assertIsNone(tag.a)
        self.assertIsNone(tag.b)

        TagD = defaultify_init(Tag, 'Tagd', a=1, b=2)
        tagD = TagD()
        self.assertEqual(tagD.a, 1)
        self.assertEqual(tagD.b, 2)

        tagD2 = TagD(b=4)
        self.assertEqual(tagD2.a, 1)
        self.assertEqual(tagD2.b, 4)

        tagD3 = TagD(a=4)
        self.assertEqual(tagD3.a, 4)
        self.assertEqual(tagD3.b, 2)

        tagD4 = TagD(a=5, b=6)
        self.assertEqual(tagD4.a, 5)
        self.assertEqual(tagD4.b, 6)

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

        TagL = xmltuple('Tag', 'tag', ['tag1', 'tag2'], (Tag1, Tag2))
        tagL = TagL.from_xml(tag.to_xml())
        self.assertEqual(tag.to_xml(), tagL.to_xml())

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

    def test_enum(self):
        Enum = xmlenum('Enum', 'enum', a='a', b='b', c='c')
        a1 = Enum(Enum.a)
        a2 = Enum(Enum.a)
        b = Enum(Enum.b)

        self.assertEqual(a1, a2)
        self.assertEqual(str(a1), str(a2))
        self.assertEqual(repr(a1), repr(a2))
        self.assertEqual(a1, Enum.a)
        self.assertNotEqual(a1, b)
        self.assertNotEqual(a1, Enum.b)

        self.assertEqual(a1.to_xml(), a2.to_xml())

        a3 = Enum(a1)
        self.assertEqual(a1, a3)

        a4 = Enum.from_xml(a1.to_xml())
        self.assertEqual(a1, a4)

    def test_all(self):
        Tag1 = xmltuple('Tag1', 'tag1', ['a'])
        Tag2 = xmltuple('Tag2', 'tag2', ['b'])
        Tag3 = xmltuple('Tag3', 'tag3', ['c'])

        All = xmlall(
            'All',
            'all',
            tags1=Tag1,
            tags2=Tag2,
            tags3=Tag3
        )

        all_ = All(tags1=[Tag1(1), Tag1(2), Tag1(3)],
                   tags2=[Tag2('a'), Tag2('b'), Tag2('c')],
                   tags3=[Tag3('x'), Tag3('y'), Tag3('z')])
        self.assertEqual(all_.to_xml(), All.from_xml(all_.to_xml()).to_xml())

        all2 = All([Tag1(1), Tag2('a'), Tag3('x'),
                    Tag1(2), Tag2('b'), Tag3('c')])
        self.assertEqual(all2.to_xml(), All.from_xml(all2.to_xml()).to_xml())
