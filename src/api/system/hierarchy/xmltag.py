from magic_repr import make_repr

from api.erd.er_entities import ConvertableXML, XMLObject

__all__ = ['xmltag']


def to_xml(self):
    tag = self.soup.new_tag(self._tag_name)
    tag.string = str(self.value)
    return tag


def to_object(self, add_name=False):
    if not add_name:
        return self.value
    res = {}
    res[self._tag_name] = self.value
    return res


def xmltag(classname, tag_name, type_):
    class_ = type(
        classname, (XMLObject, ConvertableXML), {
            "__init__":
                lambda self, value: setattr(self, 'value', type_(value)),
            "to_xml":
                to_xml,
            "_from_xml":
                classmethod(lambda cls, tag: cls._make_args(tag.text)),
            "to_object":
                to_object,
            "_tag_name": tag_name,
            "__str__":
                lambda self: str(self.value)
        }
    )
    class_.__repr__ = make_repr('value')
    return class_
