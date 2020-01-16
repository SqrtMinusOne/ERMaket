from magic_repr import make_repr

from .attribute import Attribute
from .xml_object import XMLObject

__all__ = ['Entity']


class Entity(XMLObject):
    def __init__(self, _id, name, attributes):
        self._id = _id
        self.name = name
        self.attributes = attributes

    @property
    def _tag_name(self):
        return 'entity'

    @classmethod
    def _from_xml(cls, tag):
        attributes = [Attribute.from_xml(t) for t in tag.find_all('attribute')]
        return cls._make_args(
            _id=int(tag['id']),
            name=tag.find('name').text,
            attributes=attributes
        )

    def to_xml(self):
        tag = self.soup.new_tag(self._tag_name, id=self._id)
        tag.append(self.new_tag('name', self.name))
        [tag.append(attr.to_xml()) for attr in self.attributes]
        return tag


Entity.__repr__ = make_repr('_id', 'name', 'attributes')
