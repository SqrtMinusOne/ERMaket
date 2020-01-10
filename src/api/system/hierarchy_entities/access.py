from enum import IntEnum

from api.erd.er_entities import XMLObject

from .xmllist import xmllist

__all__ = ['AccessRight', 'RoleAccess', 'AccessRights']


class AccessRight(IntEnum):
    VIEW = 0
    CHANGE = 1
    DELETE = 2


class RoleAccess(XMLObject):
    _access_texts = ['view', 'change', 'delete']

    def __init__(self, role_name, access_types):
        self.role_name = role_name
        self.access_types = set(access_types)

    def to_xml(self):
        tag = self.soup.new_tag('roleAccess')
        tag.append(self.new_tag('roleName', self.role_name))
        [
            tag.append(
                self.new_tag('access', self._access_texts[access_type])
            ) for access_type in self.access_types
        ]
        return tag

    @classmethod
    def from_xml(cls, tag):
        return cls(
            tag.roleName.text,
            {
                AccessRight(cls._access_texts.index(access.text))
                for access in tag.find_all('access')
            }
        )


AccessRights = xmllist('AccessRights', 'accessRights', RoleAccess, ['inherit'])
