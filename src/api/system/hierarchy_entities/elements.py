from .access import AccessRights
from .xmllist import xmllist
from .xmltuple import xmltuple

__all__ = ['Button', 'Trigger', 'Buttons', 'Triggers', 'Children', 'Section']

# Buttons
Button = xmltuple('Button', 'button', ['text', 'location'])
Buttons = xmllist('Buttons', 'buttonList', Button)

# Triggers
Trigger = xmltuple('Trigger', 'button', ['activation', 'scriptId'])
Triggers = xmllist('Triggers', 'triggerList', Trigger)

# Abstract hierarchy element params
_element_attrs = ['id', 'accessRights', 'buttonList', 'triggerList', 'name']
_element_children_classes = {
    'accessRights': AccessRights,
    'buttonList': Buttons,
    'triggerList': Triggers
}
_element_kws = ['id']

# Hierachy section
Children = xmllist('Children', 'children', 'childId')
Section = xmltuple(
    'Section', 'section', [*_element_attrs, 'children'],
    _element_children_classes, _element_kws
)
