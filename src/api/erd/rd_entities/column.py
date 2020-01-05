from magic_repr import make_repr

__all__ = ['Column']


class Column:
    def __init__(self,
                 name,
                 type_,
                 not_null=False,
                 auto_inc=False,
                 unique=False,
                 pk=False):
        self.name = name
        self.type_ = type_
        self.not_null = not_null
        self.auto_inc = auto_inc
        self.unique = unique
        self.pk = pk


Column.__repr__ = make_repr('name', 'type_', 'not_null', 'auto_inc', 'unique',
                            'pk')
