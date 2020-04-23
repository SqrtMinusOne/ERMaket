from magic_repr import make_repr

from .attribute import Attribute
from ermaket.utils.xml import XMLObject

__all__ = ['Entity']


class Entity(XMLObject):
    def __init__(self, _id, name, attributes, system_table=None):
        self._id = _id
        self.name = name
        self.attributes = attributes
        self.system_table = system_table

    @property
    def _tag_name(self):
        return 'entity'

    @classmethod
    def _from_xml(cls, tag):
        attributes = [Attribute.from_xml(t) for t in tag.find_all('attribute')]
        system_table = tag.find('systemTable')
        if system_table:
            system_table = system_table.text
        return cls._make_args(
            _id=int(tag['id']),
            name=tag.find('name').text,
            system_table=system_table,
            attributes=attributes
        )

    def to_xml(self):
        tag = self.soup.new_tag(self._tag_name, id=self._id)
        tag.append(self.new_tag('name', self.name))
        if self.system_table:
            tag.append(self.new_tag('systemTable', self.system_table))
        [tag.append(attr.to_xml()) for attr in self.attributes]
        return tag


Entity.__repr__ = make_repr('_id', 'name', 'attributes')
