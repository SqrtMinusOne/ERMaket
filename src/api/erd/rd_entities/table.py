from typing import List, Union

from magic_repr import make_repr

from .column import Column

__all__ = ['Table']


class Table:
    def __init__(self, name, columns: List[Column]):
        self.name = name
        self.columns = columns
        self.foreign_keys = []

    def add_fk(self, fk):
        self.foreign_keys.append(fk)

    @property
    def pk(self) -> Union[Column, List[Column]]:
        pks = [column for column in self.columns if column.pk]
        if len(pks) == 0:
            return None
        if len(pks) == 1:
            return pks[0]
        return pks


Table.__repr__ = make_repr('name', 'columns', 'foreign_keys')
