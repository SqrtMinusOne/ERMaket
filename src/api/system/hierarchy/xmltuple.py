from magic_repr import make_repr

from api.erd.er_entities import XMLObject

__all__ = ['xmltuple', 'make_to_xml']


class TextTag:
    @classmethod
    def from_xml(cls, tag):
        return tag.text


def make_to_xml(tag_name, attributes, kws=None):
    if kws is None:
        kws = []

    def to_xml(self):
        tag = self.soup.new_tag(tag_name)
        for key in attributes + kws:
            value = getattr(self, key)
            if isinstance(value, XMLObject):
                tag.append(value.to_xml())
            elif kws and key in kws and value is not None:
                tag[key] = value
            elif value is not None:
                tag.append(self.new_tag(key, value))
        return tag

    return to_xml


def make_from_xml(children_classes):
    children_classes = {} if children_classes is None else children_classes

    @classmethod
    def from_xml(cls, tag):
        attrs = {
            child.name: children_classes.get(child.name,
                                             TextTag).from_xml(child)
            for child in tag.find_all(True, recursive=False)
        }
        return cls._make_args(**attrs, **tag.attrs)

    return from_xml


def try_cast(key, value, types):
    type_ = types.get(key)
    if type_ is not None:
        return type_(value)
    return value


def make_init(attributes, types):
    def __init__(self, *args, **kwargs):
        [setattr(self, key, None) for key in attributes]
        [
            setattr(self, key, try_cast(key, value, types))
            for key, value in zip(attributes, args)
        ]
        [
            setattr(self, key, try_cast(key, value, types))
            for key, value in kwargs.items()
        ]

    return __init__


def xmltuple(
    classname, tag_name, attributes, children_classes=None, kws=[], types={}
):
    if isinstance(children_classes, (list, tuple)):
        children_classes = {c_._tag_name: c_ for c_ in children_classes}
    class_ = type(
        classname, (XMLObject, ), {
            "__init__": make_init(attributes, types),
            "to_xml": make_to_xml(tag_name, attributes, kws),
            "_from_xml": make_from_xml(children_classes),
            "_tag_name": tag_name,
            **{key: None
               for key in attributes}
        }
    )
    class_.__repr__ = make_repr(*attributes, *kws)
    return class_
