class ORMRelationship:
    def __init__(self,
                 table,
                 ref_table,
                 name,
                 fk_col=None,
                 secondary_table=None):
        self.table = table
        self.ref_table = ref_table
        self.name = name
        self.fk_col = fk_col
        self.secondary_table = secondary_table

    def __repr__(self):
        ret = f'<ORMRelationship table.name={self.table.name}'
        f', ref_table.name={self.ref_table.name}'
        f', name={self.name}'
        if self.fk_col:
            ret += f', fk_col.name={self.fk_col.name}'
        if self.secondary_table:
            ret += ', secondary_table.name={self.secondary_table.name}'
        ret += '>'
        return ret
