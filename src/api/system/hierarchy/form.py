from .elements import (_element_attrs, _element_children_classes, _element_kws,
                       _element_types)
from .xmlall import xmlall
from .xmlenum import xmlenum
from .xmltuple import xmltuple
from utils import caster

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

SimpleField = xmltuple(
    'SimpleField', 'simpleField', ['tableField', 'text', 'isEditable']
)

LinkedField = xmltuple(
    'LinkedField', 'linkedField',
    ['tableField', 'text', 'isEditable', 'linkType'], [LinkType],
    {'isEditable': caster.bool_cast}
)

FormFields = xmlall(
    'FormFields', 'fields', simple=SimpleField, linked=LinkedField
)

# TODO 16-01-20 09:03:35 conversion to form-generator schema
FormDescription = xmltuple(
    'FormDescription', 'formDescription', ['name', 'tableName', 'fields'],
    [FormFields]
)

Form = xmltuple(
    'Form', 'formEntry', [*_element_attrs, 'from'],
    [*_element_children_classes, FormDescription], _element_kws, _element_types
)
