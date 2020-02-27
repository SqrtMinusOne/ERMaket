# from magic_repr import make_repr

from utils.xml import XMLObject

__all__ = ['Side']


class Side(XMLObject):
    def __init__(self, idRef, isMandatory, isMultiple):
        self.id_ref = idRef
        self.is_mandatory = isMandatory
        self.is_multiple = isMultiple

    @property
    def _tag_name(self):
        return 'side'

    @classmethod
    def _from_xml(cls, tag):
        return cls._make_args(
            int(tag.idRef.text), tag.isMandatory.text == 'true',
            tag.isMultiple.text == 'true'
        )

    def to_xml(self):
        tag = self.soup.new_tag(self._tag_name)
        tag.append(self.new_tag('idRef', self.id_ref))
        tag.append(self.new_tag('isMandatory', str(self.is_mandatory).lower()))
        tag.append(self.new_tag('isMultiple', str(self.is_multiple).lower()))
        return tag

    def __repr__(self):
        ret = f'<Side [{self.id_ref}]: '
        if self.is_multiple:
            ret += 'N, '
        else:
            ret += '1, '
        if self.is_mandatory:
            ret += 'mandatory'
        else:
            ret += 'non-mandatory'
        ret += '>'
        return ret

# Side.__repr__ = make_repr('id_ref', 'is_mandatory', 'is_multiple')
