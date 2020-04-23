from utils.xml import xmlenum, xmllist, xmltuple

__all__ = [
    'Button', 'Buttons', 'Trigger', 'Triggers', 'Activation', 'Location',
    'SystemAction'
]

# Buttons
Location = xmlenum(
    'Location',
    'location',
    TOP='top',
    CARDHEADER='cardHeader',
    # COLUMN='column',  # In table column
    ACTION='action'  # In actions column
)

_locations = {
    "all": [Location.TOP, Location.CARDHEADER],
    "tableEntry": [Location.ACTION]
}

SystemAction = xmlenum(
    'SystemAction', 'action', REGTOKEN='regToken', PASSTOKEN='passToken'
)

Button = xmltuple(
    'Button',
    'button', [
        'text', 'location', 'icon', 'column', 'tooltip', 'variant', 'scriptId',
        'action'
    ], [Location, SystemAction],
    types={
        'scriptId': lambda v: int(v) if v is not None else None,
        'column': lambda v: int(v) if v is not None else None,
    }
)
Buttons = xmllist('Buttons', 'buttonList', Button)

# Triggers
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

_activations = {
    "all": [Activation.OPEN, Activation.AFTEROPEN],
    "tableEntry": [Activation.READ, Activation.TRANSACTION],
    "global": [Activation.LOGIN, Activation.LOGOUT]
}

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
