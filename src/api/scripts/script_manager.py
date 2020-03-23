import atexit
import importlib
import logging
import os

from api.config import Config
from api.system.hierarchy import Activation
from utils import Singleton

from .script_config import ScriptList

__all__ = ['ScriptManager', 'Context', 'ReturnContext']


class Context:
    def __init__(
        self,
        activation=Activation.CALL,
        user=None,
        elem=None,
        request_data=None,
        transaction=None,
        exec_data=None
    ):
        self.activation = Activation.CALL
        self.user = user
        self.elem = elem
        self.request_data = request_data,
        self.transaction = transaction
        self.exec_data = exec_data


class ReturnContext:
    def __init__(self, append_request=None, abort=None):
        self.append_request = {} if append_request is None else append_request
        self.abort = abort


class ScriptManager(metaclass=Singleton):
    def __init__(self, save=True, discover=False):
        self._config = Config()
        self._list = None
        self._force_discover = discover

        self._imported = {}
        self._session = None

        self.read()
        if save:
            atexit.register(lambda manager: manager.save(), self)

    def set_session(self, session):
        self._session = session

    def execute(self, id, context: Context, restart=False) -> ReturnContext:
        if '_scripts' not in self._session:
            self._session['_scripts'] = {}
        script = self._imported[id]
        if restart or id not in self._session['_scripts'] or len(script) == 1:
            self._init_script(id)
        elif (
            self._session['_scripts'][id]['index'] > 0 and
            self._session['_scripts'][id]['index'] % len(script) == 0
        ):
            self._init_script(id)

        script_data = self._session['_scripts'][id]
        context.exec_data = script_data['data']
        ret = script[script_data['index']](context)
        script_data['index'] += 1
        return ret

    def _init_script(self, id):
        self._session['_scripts'][id] = {'index': 0, 'data': {}}

    def read(self):
        if os.path.exists(
            self._config.XML['scriptsPath']
        ) or self._force_discover:
            with open(self._config.XML['scriptsPath']) as f:
                self._list = ScriptList(xml=f.read())
            logging.info('Read script data: {len(self._list)} scripts')
        else:
            self._force_discover = True
            self._discover()
        self._import()

    def _discover(self):
        self._list = ScriptList.discover()
        logging.info('Discovered scripts: {len(self._list)}')

    def _import(self):
        for script in self._list:
            module_name = script.path.replace('/', '.')[:-3]
            module = importlib.import_module(module_name)

            if len(module.__all__) != 1:
                raise ValueError(
                    f"Script file ({module_name}) has to export exactly"
                    "one object in __all__"
                )
            self._imported[script.id] = getattr(module, module.__all__[0])

        if self._force_discover:
            self._resolve_ids()

    def __getitem__(self, key):
        return self._imported[key]

    def _resolve_ids(self):
        id_map = {
            script.id: self._imported[script.id].id
            for script in self._list
        }
        ctr = 0
        for old_id, new_id in id_map.items():
            if new_id is None:
                while ctr in id_map.values():
                    ctr += 1
                id_map[old_id] = ctr

        new_imported = {
            new_id: self._imported[old_id]
            for old_id, new_id in id_map.items()
        }
        for script in self._list:
            script.id = id_map[script.id]
        self._imported = new_imported

    def save(self):
        with open(self._config.XML['scriptsPath'], 'w') as f:
            f.write(self._list.pretty_xml())
        try:
            logging.info(
                f'Saved scripts data. Script number: {len(self._list)}'
            )
        except ValueError:
            pass
