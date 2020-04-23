from magic_repr import make_repr

from ermaket.utils.xml import XMLObject

__all__ = ['Attribute']


class Attribute(XMLObject):
    def __init__(
        self,
        name: str,
        type_: str,
        is_pk: bool = False,
        is_null=False,
        is_display=False
    ):
        self.name = name
        self.type_ = type_
        self.is_pk = is_pk
        self.is_null = is_null
        self.is_display = is_display

    @property
    def _tag_name(self):
        return 'attribute'

    @classmethod
    def _from_xml(cls, tag):
        isPk = True if tag.isPk and tag.isPk.text == 'true' else False
        is_null = True if tag.isNull and tag.isNull.text == 'true' else False
        is_display = (
            True if tag.isDisplay and tag.isDisplay.text == 'true' else False
        )
        return cls._make_args(
            name=tag.find('name').text,
            type_=tag.type.text,
            is_pk=isPk,
            is_null=is_null,
            is_display=is_display
        )

    def to_xml(self):
        tag = self.soup.new_tag(self._tag_name)
        tag.append(self.new_tag('name', self.name))
        if self.is_pk:
            tag.append(self.new_tag('isPk', str(self.is_pk).lower()))
        if self.is_null:
            tag.append(self.new_tag('isNull', str(self.is_null).lower()))
        if self.is_display:
            tag.append(self.new_tag('isDisplay', str(self.is_display).lower()))
        tag.append(self.new_tag('type', self.type_))
        return tag


Attribute.__repr__ = make_repr('name', 'type_', 'is_pk')
