from utils import caster, defaultify_init

from .elements import (_element_attrs, _element_children_classes, _element_kws,
                       _element_types)
from .xmlall import xmlall
from .xmlenum import xmlenum
from .xmltuple import xmltuple

__all__ = [
    'LinkType', 'SimpleField', 'LinkedField', 'FormFields', 'FormDescription',
    'Form'
]

LinkType = xmlenum(
    'LinkType',
    'linkType',
    SIMPLE='simple',
    DROPDOWN='dropdown',
    LINKEDTABLE='linkedTable',
    LINKEDFORM='linkedForm',
    GROUPEDFORM='groupedForm'
)

_field_attrs = [
    'rowName', 'text', 'isEditable'
]

_field_types = {
    'isEditable': caster.bool_cast
}

SimpleField = xmltuple(
    'SimpleField', 'simpleField', _field_attrs,
    types=_field_types
)

LinkedField = xmltuple(
    'LinkedField', 'linkedField',
    [*_field_attrs, 'linkType'], [LinkType],
    types=_field_types
)

FormFields = xmlall(
    'FormFields', 'fields', simple=SimpleField, linked=LinkedField
)

# TODO 16-01-20 09:03:35 conversion to form-generator schema
_FormDescription = xmltuple(
    'FormDescription', 'formDescription', ['schema', 'tableName', 'fields'],
    [FormFields]
)

FormDescription = defaultify_init(
    _FormDescription, 'FormDescription', fields=lambda s: FormFields()
)

Form = xmltuple(
    'Form', 'formEntry', [*_element_attrs, 'formDescription'],
    [*_element_children_classes, FormDescription], _element_kws, _element_types
)
