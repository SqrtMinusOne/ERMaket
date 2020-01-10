from enum import IntEnum

from api.erd.er_entities import XMLObject

from .xmltuple import xmltuple

__all__ = [
    'LinkType', 'SimpleField', 'FormDescription', 'LinkType', 'LinkedField',
    'FormFields'
]


class LinkType(IntEnum):
    SIMPLE = 0
    DROPDOWN = 0
    LINKEDTABLE = 0


SimpleField = xmltuple(
    'SimpleField', 'simpleField', ['tableField', 'text', 'isEditable']
)


class LinkedField(SimpleField):
    _link_texts = ['simple', 'dropdown', 'linkedTable']

    def __init__(self, *args, linkType, **kwargs):
        self.linkType = linkType

    def to_xml(self):
        tag = super().to_xml()
        tag.append(self.new_tag('linkType', self._link_texts[self.linkType]))
        return tag

    @classmethod
    def from_xml(cls, tag):
        field = super(SimpleField, cls).from_xml(tag)
        field.linkType = LinkType(cls._link_texts.index(field.linkType))
        return field


class FormFields(XMLObject):
    def __init__(self, fields, linked_fields):
        self.fields = fields
        self.linked_fields = linked_fields

    def to_xml(self):
        tag = self.soup.new_tag('fields')
        [
            tag.append(field.to_xml())
            for field in [*self.fields, *self.linked_fields]
        ]
        return tag

    @classmethod
    def from_xml(cls, tag):
        return cls(
            [SimpleField.from_xml(t) for t in tag.find_all('simpleField')],
            [LinkedField.from_xml(t) for t in tag.find_all('linked_fields')]
        )


FormDescription = xmltuple(
    'FormDescription', 'formDescription', ['name', 'fields'],
    {'fields': FormFields}
)
