from utils import caster, defaultify_init

from .elements import (_element_attrs, _element_children_classes, _element_kws,
                       _element_types)
from utils.xml import xmlenum, xmllist, xmltuple, xmlall

__all__ = [
    'LinkType', 'SimpleField', 'LinkedField', 'FormFields', 'FormDescription',
    'Form', 'FormGroups', 'FormGroup'
]

LinkType = xmlenum(
    'LinkType',
    'linkType',
    SIMPLE='simple',
    DROPDOWN='dropdown',
    LINKEDTABLE='linkedTable',
    LINKEDFORM='linkedForm',
    # GROUPEDFORM='groupedForm'
)

_field_attrs = [
    'rowName', 'text', 'isEditable', 'isVisible', 'hint', 'help'
]

_field_types = {'isEditable': caster.bool_cast, 'isVisible': caster.bool_cast}

_field_defaults = {'isVisible': True}

_SimpleField = xmltuple(
    'SimpleField', 'simpleField', _field_attrs, types=_field_types
)

SimpleField = defaultify_init(_SimpleField, 'SimpleField', **_field_defaults)

_LinkedField = xmltuple(
    'LinkedField',
    'linkedField', [*_field_attrs, 'linkType'], [LinkType],
    types=_field_types
)

LinkedField = defaultify_init(_LinkedField, 'LinkedField', **_field_defaults)

FormFields = xmlall(
    'FormFields', 'fields', simple=SimpleField, linked=LinkedField
)

RowNames = xmllist('RowNames', 'rows', 'rowName')

_FormGroup = xmltuple('FormGroup', 'formGroup', ['legend', 'rows'], [RowNames])

FormGroup = defaultify_init(_FormGroup, 'FormGroup', rows=lambda s: RowNames())

FormGroups = xmllist('FormGroups', 'groups', FormGroup)

_FormDescription = xmltuple(
    'FormDescription', 'formDescription',
    ['schema', 'tableName', 'fields', 'groups'], [FormFields, FormGroups]
)

FormDescription = defaultify_init(
    _FormDescription,
    'FormDescription',
    fields=lambda s: FormFields(),
    groups=lambda s: FormGroups()
)

Form = xmltuple(
    'Form', 'formEntry', [*_element_attrs, 'formDescription'],
    [*_element_children_classes, FormDescription], _element_kws, _element_types
)
