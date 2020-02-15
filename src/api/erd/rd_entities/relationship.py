class ORMRelationship:
    def __init__(
        self,
        table,
        ref_table,
        name,
        relation,
        side_index,
        ref_rel=None,
        fk_col=None,
        secondary_table=None,
    ):
        self.table = table
        self.ref_table = ref_table
        self.name = name
        self.relation = relation
        self.side_index = side_index
        self.ref_rel = ref_rel
        self.fk_col = fk_col
        self.secondary_table = secondary_table

    @property
    def ref_rel(self):
        return self._ref_rel

    @ref_rel.setter
    def ref_rel(self, value):
        self._ref_rel = value
        if self._ref_rel:
            self._ref_rel._ref_rel = self

    def __repr__(self):
        ret = f'<ORMRelationship table.name={self.table.name}'
        ret += f', ref_table.name={self.ref_table.name}'
        ret += f', name={self.name}'
        ret += f', relation.name={self.relation.name}'
        ret += f', side_index={self.side_index}'
        if self.fk_col:
            ret += f', fk_col.name={self.fk_col.name}'
        if self.secondary_table:
            ret += f', secondary_table.name={self.secondary_table.name}'
        ret += '>'
        return ret
