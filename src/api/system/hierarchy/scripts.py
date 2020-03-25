from utils.xml import xmlenum, xmllist, xmltuple

__all__ = ['Button', 'Buttons', 'Trigger', 'Triggers', 'Activation']

# Buttons
Location = xmlenum('Location', 'location', TOP='top', CARDHEADER='cardHeader')

Button = xmltuple(
    'Button',
    'button', ['text', 'location', 'variant', 'scriptId'], [Location],
    types={'scriptId': int}
)
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
        self._triggers = {}
        self._sort_scripts()

    def _sort_scripts(self):
        for trigger in self:
            try:
                self._triggers[str(trigger.activation)].append(
                    trigger.scriptId
                )
            except KeyError:
                self._triggers[str(trigger.activation)] = [trigger.scriptId]

    def get_scripts(self, activation):
        return self._triggers.get(str(activation), [])

    def append(self, *args, **kwargs):
        super().append(*args, **kwargs)
        self._sort_scripts()
