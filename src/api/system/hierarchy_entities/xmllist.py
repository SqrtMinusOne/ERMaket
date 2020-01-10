from magic_repr import make_repr

from api.erd.er_entities import XMLObject

__all__ = ['xmllist']


def __init__(self, values):
    self.values = values


def make_to_xml(tag_name, children_class, children_tag):
    def to_xml(self):
        tag = self.soup.new_tag(tag_name)
        if children_class is not None:
            [tag.append(value.to_xml()) for value in self.values]
        else:
            [
                tag.append(self.new_tag(children_tag, value))
                for value in self.values
            ]
        return tag

    return to_xml


def make_from_xml(children_class):
    @classmethod
    def from_xml(cls, tag):
        if children_class is not None:
            values = [children_class.from_xml(child) for child in tag.children]
        else:
            values = [child.text for child in tag.children]
        return cls(values=values)
    return from_xml


def xmllist(classname, tag_name, children):
    children_class, children_tag = None, None
    if isinstance(children, type):
        children_class = children
    else:
        children_tag = children
    class_ = type(
        classname, (XMLObject, ), {
            "__init__":
                __init__,
            "to_xml":
                make_to_xml(tag_name, children_class, children_tag),
            "from_xml":
                make_from_xml(children_class),
            "values": [],
            "__len__":
                lambda self: len(self.values),
            "__getitem__":
                lambda self, key: self.values.__getitem__(key),
            "__setitem__":
                lambda self, key, value: self.values.__setitem__(key, value),
            "__delitem__":
                lambda self, key: self.values.__delitem__(key),
            "__iter__":
                lambda self: self.value.__iter__
        }
    )
    class_.__repr__ = make_repr('values')
    return class_
