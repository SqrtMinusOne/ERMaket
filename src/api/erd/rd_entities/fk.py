from .column import Column
from .table import Table

__all__ = ['ForeignKey']


class ForeignKey:
    def __init__(self,
                 table: Table,
                 column: Column = None,
                 name=None,
                 onupdate='cascade',
                 ondelete='cascade',
                 unique=False):
        self.table = table
        self.column = column
        self.name = name
        self.onupdate, self.ondelete = onupdate, ondelete
        self.unique = unique

    def __repr__(self):
        if self.column is not None:
            column_name = self.column.name
        else:
            column_name = "unresolved"
            repr_ = (f'<ForeignKey table_name="{self.table.name}"'
                     f' column_name="{column_name}"')
        if self.name is not None:
            repr_ += f' name="{self.name}"'
        if self.ondelete != "cascade":
            repr_ += f' ondelete="{self.ondelete}"'
        if self.onupdate != "cascade":
            repr_ += f' onupdate="{self.onupdate}"'
        if self.unique:
            repr_ += f' unique={self.unique}'
        repr_ += '>'
        return repr_
