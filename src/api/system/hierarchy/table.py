from utils import caster, defaultify_init

from .elements import (_element_attrs, _element_children_classes, _element_kws,
                       _element_types)
from .form import FormDescription
from .xmllist import xmllist
from .xmltuple import xmltuple

__all__ = ['Table', 'TableColumn', 'TableColumns']

_TableColumn = xmltuple(
    '_TableColumn',
    'column', ['rowName', 'text', 'isSort', 'isFilter'],
    types={
        'isSort': caster.bool_cast,
        'isFilter': caster.bool_cast
    }
)

TableColumn = defaultify_init(
    _TableColumn,
    'TableColumn',
    text=lambda s: s.rowName,
    isSort=True,
    isFilter=True
)

TableColumns = xmllist('TableColumns', 'columns', TableColumn)

__Table = xmltuple(
    '__Table', 'tableEntry',
    [*_element_attrs, 'tableName', 'schema', 'linesOnPage', 'columns', 'form'],
    [*_element_children_classes, TableColumns, FormDescription], _element_kws,
    {
        **_element_types, 'linesOnPage': int
    }
)

_Table = defaultify_init(
    __Table,
    '_Table',
    linesOnPage=50,
    columns=lambda self: TableColumns(),
    tableName=lambda self: self.name,
)


class Table(_Table):
    pass  # TODO 16-01-20 13:58:45 генерация формы
