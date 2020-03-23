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
    TRANSACTION='transaction',  # Transaction (global)
    LOGIN='login',  # Login (global)
    LOGOUT='logout',  # Logout (global)
    CALL='call'  # For internal use
)

# Triggers
Trigger = xmltuple(
    'Trigger',
    'trigger', ['activation', 'scriptId'], [Activation],
    types={'scriptId': int}
)
_Triggers = xmllist('Triggers', 'triggerList', Trigger)


class Triggers(_Triggers):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scripts = {}
        self._sort_scripts()

    def _sort_scripts(self):
        for script in self:
            try:
                self._scripts[script.activation].append(script.id)
            except KeyError:
                self._scripts[script.activation] = [script.id]

    def get_scripts(self, activation):
        return self._scripts.get(activation, [])
