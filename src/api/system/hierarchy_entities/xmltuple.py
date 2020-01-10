from magic_repr import make_repr

from api.erd.er_entities import XMLObject

__all__ = ['xmltuple', 'make_to_xml']


class TextTag:
    @classmethod
    def from_xml(cls, tag):
        return tag.text


def make_to_xml(tag_name, attributes, kws):
    def to_xml(self):
        tag = self.soup.new_tag(tag_name)
        for key in attributes:
            value = getattr(self, key)
            if isinstance(value, XMLObject):
                tag.append(value.to_xml())
            elif kws and key in kws:
                tag[key] = value
            else:
                tag.append(self.new_tag(key, value))
        return tag

    return to_xml


def make_from_xml(children_classes):
    children_classes = {} if children_classes is None else children_classes

    @classmethod
    def from_xml(cls, tag):
        attrs = {
            child.name:
            children_classes.get(child.name, TextTag).from_xml(child)
            for child in tag.children
        }
        return cls(**attrs, **tag.attrs)

    return from_xml


def make_init(attributes):
    def __init__(self, *args, **kwargs):
        [setattr(self, key, None) for key in attributes]
        [setattr(self, key, value) for key, value in zip(attributes, args)]
        [setattr(self, key, value) for key, value in kwargs.items()]

    return __init__


def xmltuple(classname, tag_name, attributes, children_classes=None, kws=None):
    class_ = type(
        classname, (XMLObject, ), {
            "__init__": make_init(attributes),
            "to_xml": make_to_xml(tag_name, attributes, kws),
            "from_xml": make_from_xml(children_classes),
            **{key: None
               for key in attributes}
        }
    )
    class_.__repr__ = make_repr(*attributes)
    return class_
