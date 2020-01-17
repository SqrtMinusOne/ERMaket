from .access import AccessRights
from .xmlenum import xmlenum
from .xmllist import xmllist
from .xmltuple import xmltuple

__all__ = [
    'Button', 'Trigger', 'Buttons', 'Triggers', 'Page',
    'PrebuiltPageType', 'PrebuiltPage'
]

# Buttons
Button = xmltuple('Button', 'button', ['text', 'location'])
Buttons = xmllist('Buttons', 'buttonList', Button)

# Triggers
Trigger = xmltuple('Trigger', 'trigger', ['activation', 'scriptId'])
Triggers = xmllist('Triggers', 'triggerList', Trigger)

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
    [*_element_children_classes, PrebuiltPageType], _element_types
)
