from api.erd.er_entities import XMLObject

from .xmlenum import xmlenum
from .xmllist import xmllist

__all__ = ['AccessRight', 'RoleAccess', 'AccessRights']

AccessRight = xmlenum(
    'AccessRight', 'access', VIEW='view', CHANGE='change', DELETE='delete'
)


class RoleAccess(XMLObject):
    def __init__(self, role_name, access_types):
        self.role_name = role_name
        self.access_types = set(AccessRight(t) for t in access_types)

    def to_xml(self):
        tag = self.soup.new_tag('roleAccess')
        tag.append(self.new_tag('roleName', self.role_name))
        [tag.append(access_type.to_xml()) for access_type in self.access_types]
        return tag

    @classmethod
    def _from_xml(cls, tag):
        return cls._make_args(
            tag.roleName.text,
            [AccessRight(t) for t in tag.find_all(AccessRight._tag_name)]
        )


_AccessRights = xmllist(
    'AccessRights', 'accessRights', RoleAccess, ['inherit']
)


class AccessRights(_AccessRights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == len(kwargs) == 0:
            self.inherit = True
        elif not self.inherit:
            self.inherit = False
