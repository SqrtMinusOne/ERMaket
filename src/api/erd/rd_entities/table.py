from typing import List

from magic_repr import make_repr

from .column import Column

__all__ = ['Table']


class Table:
    def __init__(self, name, columns: List[Column]):
        self.name = name
        self.columns = columns


Table.__repr__ = make_repr('name', 'columns')
