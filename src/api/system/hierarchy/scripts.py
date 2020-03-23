from utils.xml import xmlenum, xmllist, xmltuple

__all__ = ['Button', 'Buttons', 'Trigger', 'Triggers', 'Activation']

# Buttons
Button = xmltuple('Button', 'button', ['text', 'location'])
Buttons = xmllist('Buttons', 'buttonList', Button)

# Script activation
Activation = xmlenum(
    'Activation',
    'activation',
    OPEN='open',  # Before opening the hierarchy element
    AFTEROPEN='afterOpen',  # After opening the hierarchy element
    READ='read',  # Read this table
    TRANSACTION='transaction',  # Transaction to this table
    LOGIN='login',
    LOGOUT='logout',
    CALL='call'  # For internal use
)

# Triggers
Trigger = xmltuple(
    'Trigger', 'trigger', ['activation', 'scriptId'], types={'scriptId': int}
)
Triggers = xmllist('Triggers', 'triggerList', Trigger)
