from magic_repr import make_repr

from api.erd.er_entities import XMLObject

__all__ = ['xmlall']


def make_init(params):
    def __init__(self, *args, **kwargs):
        [setattr(self, key, None) for key in params.keys()]
        [setattr(self, key, value) for key, value in zip(params.keys(), args)]
        [setattr(self, key, value) for key, value in kwargs.items()]

    return __init__


def make_to_xml(tag_name, params):
    def to_xml(self):
        tag = self.soup.new_tag(tag_name)
        [
            [tag.append(val.to_xml()) for val in getattr(self, attr)]
            for attr in params.keys()
        ]
        return tag

    return to_xml


def make_from_xml(params):
    @classmethod
    def from_xml(cls, tag):
        return cls._make_args(
            *[
                [class_.from_xml(t) for t in tag.find_all(class_._tag_name)]
                for attr, class_ in params.items()
            ]
        )

    return from_xml


def xmlall(classname, tag_name, **params):
    class_ = type(
        classname, (XMLObject, ), {
            "__init__": make_init(params),
            "to_xml": make_to_xml(tag_name, params),
            "_from_xml": make_from_xml(params),
            "_tag_name": tag_name
        }
    )
    class_.__repr__ = make_repr(*params.keys())
    return class_
