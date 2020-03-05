import stringcase
from utils import caster, defaultify_init

from .elements import (_element_attrs, _element_children_classes, _element_kws,
                       _element_types)
from .form import (FormDescription, FormGroup, LinkedField, LinkType,
                   SimpleField)
from utils.xml import xmlall, xmltuple, xmlenum

__all__ = [
    'Table', 'TableColumn', 'TableColumns', 'TableLinkType',
    'LinkedTableColumn'
]

_table_column_attrs = [
    'rowName', 'text', 'isSort', 'isFilter', 'isEditable', 'isPk',
    'isRequired', 'type', 'dateFormat', 'isVisible', 'isUnique', 'isAuto',
    'default'
]

_table_column_types = {
    'isPk': caster.bool_cast,
    'isSort': caster.bool_cast,
    'isFilter': caster.bool_cast,
    'isEditable': caster.bool_cast,
    'isRequired': caster.bool_cast,
    'isVisible': caster.bool_cast,
    'isUnique': caster.bool_cast,
    'isAuto': caster.bool_cast
}

_TableColumn = xmltuple(
    '_TableColumn',
    'column',
    _table_column_attrs,
    types=_table_column_types,
)

TableColumn = defaultify_init(
    _TableColumn,
    'TableColumn',
    text=lambda s: stringcase.sentencecase(s.rowName),
    isPk=False,
    isRequired=False,
    isSort=True,
    isFilter=True,
    isEditable=True,
    isUnique=False,
    isVisible=True,
    isAuto=False
)

TableLinkType = xmlenum(
    'TableLinkType',
    'linkType',
    SIMPLE='simple',
    DROPDOWN='dropdown',
    COMBINED='combined',
    LINKED='linked'
)

_link_type_mappings = {}
_link_type_mappings[TableLinkType.SIMPLE] = LinkType.SIMPLE
_link_type_mappings[TableLinkType.DROPDOWN] = LinkType.DROPDOWN
_link_type_mappings[TableLinkType.LINKED] = LinkType.LINKEDTABLE
_link_type_mappings[TableLinkType.COMBINED] = LinkType.LINKEDTABLE

_LinkedTableColumn = xmltuple(
    '_LinkedTableColumn',
    'linkedColumn', [
        *_table_column_attrs,
        'linkTableName',
        'linkSchema',
        'linkType',
        'fkName',
        'isMultiple',
        'linkRequired',
        'linkMultiple'
    ], [TableLinkType],
    types={
        **_table_column_types,
        'isMultiple': caster.bool_cast,
        'linkRequired': caster.bool_cast,
        'linkMultiple': caster.bool_cast
    }
)

LinkedTableColumn = defaultify_init(
    _LinkedTableColumn,
    'LinkedTableColumn',
    text=lambda s: stringcase.sentencecase(s.rowName),
    isPk=False,
    isSort=True,
    isFilter=True,
    isEditable=True,
    isAuto=False,
    isVisible=True,
    isRequired=False,
    linkRequired=False,
    linkMultiple=False,
    type='link',
    isUnique=False,
    linkType=lambda s: TableLinkType(TableLinkType.SIMPLE)
    if s.fkName else TableLinkType(TableLinkType.LINKED)
)

TableColumns = xmlall(
    'TableColumns', 'columns', normal=TableColumn, linked=LinkedTableColumn
)

__Table = xmltuple(
    '__Table', 'tableEntry', [
        *_element_attrs, 'tableName', 'schema', 'linesOnPage', 'columns',
        'formDescription', 'pagination', 'hidden'
    ], [*_element_children_classes, TableColumns, FormDescription],
    _element_kws, {
        **_element_types,
        'linesOnPage': int,
        'pagination': caster.bool_cast,
        'hidden': caster.bool_cast,
    }
)

_Table = defaultify_init(
    __Table,
    '_Table',
    linesOnPage=50,
    columns=lambda self: TableColumns(),
    tableName=lambda self: self.name,
    pagination=True,
    hidden=False
)


class Table(_Table):
    def make_form(self):
        form = FormDescription(self.schema, self.tableName)
        group = FormGroup(legend=self.name)
        for column in self.columns:
            attrs = {
                'rowName': column.rowName,
                'text': column.text,
                'isEditable': column.isEditable
            }
            if column._tag_name == 'column':
                form.fields.append(SimpleField(**attrs))
            else:
                form.fields.append(
                    LinkedField(
                        **attrs,
                        linkType=_link_type_mappings[column.linkType.value],
                    )
                )
            group.rows.append(column.rowName)
        form.groups.append(group)
        return form

    @property
    def pk(self):
        for column in self.columns:
            if column.isPk:
                return column
