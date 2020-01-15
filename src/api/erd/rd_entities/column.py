from magic_repr import make_repr

__all__ = ['Column']


class Column:
    def __init__(
        self,
        name=None,
        type_=None,
        not_null=True,
        auto_inc=False,
        unique=False,
        pk=False,
        fk=None
    ):
        self.name = name
        self.type_ = type_
        self._not_null = not_null
        self.auto_inc = auto_inc
        self._unique = unique
        self.pk = pk
        self.fk = fk

    @property
    def not_null(self):
        return self._not_null if not self.pk else True

    @property
    def unique(self):
        if self.pk and self.fk is None:
            return True
        return self._unique

    def resolve_type(self):
        self.type_ = self.fk.column.type_


Column.__repr__ = make_repr(
    'name', 'type_', 'not_null', 'auto_inc', 'unique', 'pk', 'fk'
)
