from .elements import _element_attrs, _element_children_classes, _element_kws
from .form import FormDescription
from .xmllist import xmllist
from .xmltuple import xmltuple
from utils import defaultify_init

__all__ = ['Table']

TableColumn = xmltuple(
    'TableColumn', 'column', ['rowName', 'text', 'isSort', 'isFilter']
)

TableColumns = xmllist('TableColumns', 'columns', TableColumn)

__Table = xmltuple(
    '__Table', 'tableEntry',
    [*_element_attrs, 'tableName', 'linesOnPage', 'columns', 'form'],
    [*_element_children_classes, TableColumns, FormDescription], _element_kws
)

_Table = defaultify_init(__Table, '_Table', linesOnPage=50)


class Table(_Table):
    pass  # TODO 16-01-20 13:58:45 генерация формы
