from .elements import (
    _element_attrs, _element_children_classes, _element_kws, _element_types
)
from ermaket.utils.xml import xmllist, xmltuple, xmltag

__all__ = ['Section', 'Children']

ChildId = xmltag('ChildId', 'childId', int)
Children = xmllist('Children', 'children', ChildId)
_Section = xmltuple(
    '_Section', 'section', [*_element_attrs, 'children'],
    [*_element_children_classes, Children], _element_kws, _element_types
)


class Section(_Section):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.children is None:
            self.children = Children()
        self._children = None

    def resolve_children(self, func):
        self._children = []
        for child_id in self.children:
            child = func(child_id)
            if child:
                self._children.append(child)
        return self.children.values

    def set_child_ids(self, ids):
        self._children = None
        self.children = Children([ChildId(id) for id in ids])

    def map_ids(self, mapper):
        self.children = Children(
            [ChildId(mapper(child.value)) for child in self.children]
        )

    def resolve_rights(self):
        for child in self._children:
            if child.accessRights.inherit:
                child.accessRights.copy_rights(self.accessRights)
            if isinstance(child, Section):
                child.resolve_rights()

    def to_object(self, add_name=True, add_children=False):
        obj = super().to_object(add_name)
        if add_children:
            if self._children:
                obj['children'] = [
                    child.to_object() for child in self._children
                ]
        else:
            obj['children'] = [childId.value for childId in self.children]
        return obj
