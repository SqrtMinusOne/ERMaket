from utils.xml import xmlenum, xmltuple

from .access import AccessRights
from .scripts import Buttons, Triggers

__all__ = [
    'Page', 'PrebuiltPageType',
    'PrebuiltPage'
]

# Abstract hierarchy element params
_element_attrs = ['accessRights', 'buttonList', 'triggerList', 'name']
_element_children_classes = [AccessRights, Buttons, Triggers]
_element_kws = ['id']
_element_types = {'id': int}

# User page entry
Page = xmltuple(
    'Page', 'pageEntry', [*_element_attrs, 'componentName'],
    _element_children_classes, _element_types
)

# Prebuilt pages
PrebuiltPageType = xmlenum(
    'PrebuiltPageType', 'type', SQL='sql', USERS='users', STATUS='status'
)

PrebuiltPage = xmltuple(
    'PrebuiltPage', 'prebuiltPageEntry', [*_element_attrs, 'type'],
    [*_element_children_classes, PrebuiltPageType], _element_kws,
    _element_types
)
