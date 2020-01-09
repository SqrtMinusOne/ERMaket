from .column import Column
from .table import Table

__all__ = ['ForeignKey']


class ForeignKey:
    def __init__(self,
                 table: Table,
                 column: Column = None,
                 onupdate='cascade',
                 ondelete='cascade',
                 relation_name=None,
                 add_rel=True):
        self.table = table
        self.column = column
        self.onupdate, self.ondelete = onupdate, ondelete
        self.relation_name = relation_name
        self.add_rel = add_rel

    def __repr__(self):
        if self.column is not None:
            column_name = self.column.name
        else:
            column_name = "unresolved"
        repr_ = (f'<ForeignKey table_name="{self.table.name}"'
                 f' column_name="{column_name}"')
        if self.ondelete != "cascade":
            repr_ += f' ondelete="{self.ondelete}"'
        if self.onupdate != "cascade":
            repr_ += f' onupdate="{self.onupdate}"'
        repr_ += '>'
        return repr_
