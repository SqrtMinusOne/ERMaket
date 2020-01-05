from magic_repr import make_repr

from .xml_object import XMLObject

__all__ = ['Side']


class Side(XMLObject):
    def __init__(self, idRef, isMandatory, isMultiple):
        self.id_ref = idRef
        self.is_mandatory = isMandatory
        self.is_multiple = isMultiple

    @classmethod
    def from_xml(cls, tag):
        return cls(int(tag.idRef.text), tag.isMandatory.text == 'true',
                   tag.isMultiple.text == 'true')

    def to_xml(self):
        tag = self.soup.new_tag('side')
        tag.append(self.new_tag('idRef', self.id_ref))
        tag.append(self.new_tag('isMandatory', str(self.is_mandatory).lower()))
        tag.append(self.new_tag('isMultiple', str(self.is_multiple).lower()))
        return tag


Side.__repr__ = make_repr('id_ref', 'is_mandatory', 'is_multiple')
