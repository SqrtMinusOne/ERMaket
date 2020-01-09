class Secondary:
    def __init__(self, ref_table, link_table, backref_table, relation_name):
        self.ref_table = ref_table
        self.link_table = link_table
        self.backref_table = backref_table
        self.relation_name = relation_name

    def __repr__(self):
        return f'<Secondary ref_table.name={self.ref_table.name}'
        f', link_table.name={self.link_table.name}'
        f', backref_table.name={self.backref_table.name}>'
        f', relation_name={self.relation_name}>'
