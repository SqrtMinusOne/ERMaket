from magic_repr import make_repr

from api.erd.er_entities import XMLObject, ConvertableXML

from .xmlenum import xmlenum
from .xmllist import xmllist

__all__ = ['AccessRight', 'RoleAccess', 'AccessRights']

AccessRight = xmlenum(
    'AccessRight', 'access', VIEW='view', CHANGE='change', DELETE='delete'
)


class RoleAccess(XMLObject, ConvertableXML):
    def __init__(self, role_name, access_types):
        self.role_name = role_name
        self.access_types = set(AccessRight(t) for t in access_types)

    @property
    def _tag_name(self):
        return 'roleAccess'

    def to_xml(self):
        tag = self.soup.new_tag(self._tag_name)
        tag.append(self.new_tag('roleName', self.role_name))
        [tag.append(access_type.to_xml()) for access_type in self.access_types]
        return tag

    @classmethod
    def _from_xml(cls, tag):
        return cls._make_args(
            tag.roleName.text,
            [AccessRight(t.text) for t in tag.find_all(AccessRight._tag_name)]
        )

    def to_object(self, add_name=False):
        res = {
            "role": self.role_name,
            "access": [t.to_object() for t in self.access_types]
        }
        if add_name:
            res['_tag_name'] = self._tag_name
        return res


RoleAccess.__repr__ = make_repr('role_name', 'access_types')

_AccessRights = xmllist(
    'AccessRights', 'accessRights', RoleAccess, kws=['inherit']
)


class AccessRights(_AccessRights):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(args) == len(kwargs) == 0:
            self.inherit = True
        elif not self.inherit:
            self.inherit = False
        else:
            self.inherit = self.inherit == 'True' or self.inherit is True

    def copy_rights(self, other):
        self.values = list(other.values)

    def get(self, role):
        for roleAccess in iter(self):
            if roleAccess.role_name == role:
                return list(roleAccess.access_types)
        return []

    @classmethod
    def from_xml(cls, tag):
        ret = super().from_xml(tag)
        return ret

    def to_xml(self):
        if not self.inherit:
            return super().to_xml()
        tag = self.soup.new_tag(self._tag_name)
        tag['inherit'] = True
        return tag
