from magic_repr import make_repr

from api.erd.er_entities import XMLObject

__all__ = ['xmlenum']


def make_init(classname, enums):
    def __init__(self, value):
        if type(value).__name__ == classname:
            self.key = value.key
            self.value = value.value
        else:
            self.value = value
            for k, v in enums.items():
                if v == value:
                    self.key = k
                    return
            raise ValueError(f'Value "{value}" not found in xmlenum')

    return __init__


def make_from_xml(enums):
    @classmethod
    def from_xml(cls, tag):
        for key, value in enums.items():
            if tag.text == value:
                return cls._make_args(key)
        raise ValueError(f'Key {key} not found in {cls}')

    return from_xml


def make_to_xml(tag_name):
    def to_xml(self):
        tag = self.soup.new_tag(tag_name)
        tag.string = str(self.value)
        return tag

    return to_xml


def make_eq(classname):
    def __eq__(self, other):
        if type(other).__name__ == classname:
            return other.key == self.key
        return self.value == other

    return __eq__


def __str__(self):
    return self.value


def make_hash(enums):
    hashes = {key: i for i, key in enumerate(enums.values())}

    def __hash__(self):
        return hashes[self.value]

    return __hash__


def xmlenum(classname, tag_name, **enums):
    class_ = type(
        classname, (XMLObject, ), {
            "__init__": make_init(classname, enums),
            "to_xml": make_to_xml(tag_name),
            "_from_xml": make_from_xml(enums),
            "__eq__": make_eq(classname),
            "__str__": __str__,
            "_tag_name": tag_name,
            "__hash__": make_hash(enums),
            **enums
        }
    )
    class_.__repr__ = make_repr('key')
    return class_
