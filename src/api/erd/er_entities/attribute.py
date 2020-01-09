from magic_repr import make_repr

from .xml_object import XMLObject

__all__ = ['Attribute']


class Attribute(XMLObject):
    def __init__(self, name: str, type_: str, is_pk: bool = False):
        self.name = name
        self.type_ = type_
        self.is_pk = is_pk

    @classmethod
    def from_xml(cls, tag):
        isPk = True if tag.isPk and tag.isPk.text == 'true' else False
        return cls(name=tag.find('name').text, type_=tag.type.text, is_pk=isPk)

    def to_xml(self):
        tag = self.soup.new_tag('attribute')
        tag.append(self.new_tag('name', self.name))
        if self.is_pk:
            tag.append(self.new_tag('isPk', str(self.is_pk).lower()))
        tag.append(self.new_tag('type', self.type_))
        return tag


Attribute.__repr__ = make_repr('name', 'type_', 'is_pk')
