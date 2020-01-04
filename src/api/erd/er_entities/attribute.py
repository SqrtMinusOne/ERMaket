from magic_repr import make_repr

from .xml_object import XMLObject


__all__ = ['Attribute']


class Attribute(XMLObject):
    def __init__(self, name: str, type_: str, isPk: bool = False):
        self.name = name
        self.type_ = type_
        self.isPk = isPk

    @classmethod
    def from_xml(cls, tag):
        isPk = True if tag.isPk and tag.isPk.text == 'true' else False
        return cls(name=tag.find('name').text, type_=tag.type.text, isPk=isPk)

    def to_xml(self):
        tag = self.soup.new_tag('attribute')
        tag.append(self.new_tag('name', self.name))
        if self.isPk:
            tag.append(self.new_tag('isPk', str(self.isPk).lower()))
        tag.append(self.new_tag('type', self.type_))
        return tag


Attribute.__repr__ = make_repr('name', 'type_', 'isPk')
