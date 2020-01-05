from magic_repr import make_repr

from .side import Side
from .xml_object import XMLObject


__all__ = ['Relation']


class Relation(XMLObject):
    def __init__(self, name, sides):
        self.name = name
        self.sides = sides

    @classmethod
    def from_xml(cls, tag):
        return cls(
            tag.find('name').text,
            [Side.from_xml(t) for t in tag.find_all('side')])

    def __len__(self):
        return len(self.sides)

    def invert(self):
        assert len(self.sides) == 2
        return Relation(self.name, self.sides[::-1])

    def to_xml(self):
        tag = self.soup.new_tag('relation')
        tag.append(self.new_tag('name', self.name))
        [tag.append(s.to_xml()) for s in self.sides]
        return tag


Relation.__repr__ = make_repr('name', 'sides')
