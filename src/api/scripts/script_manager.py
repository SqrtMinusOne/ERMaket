import atexit
import logging
import os

from api.config import Config
from utils import Singleton

from .script_config import ScriptList

__all__ = ['ScriptManager']


class ScriptManager(metaclass=Singleton):
    def __init__(self, save=True):
        self._config = Config()
        self._list = None

        self.read()
        if save:
            atexit.register(lambda manager: manager.save(), self)

    def read(self):
        if os.path.exists(self._config.XML['scriptsPath']):
            with open(self._config.XML['scriptsPath']) as f:
                self._list = ScriptList(xml=f.read())
            logging.info('Read script data: {len(self._list)} scripts')
        else:
            self.discover()

    def discover(self):
        self._list = ScriptList.discover()
        logging.info('Discovered scripts: {len(self._list)}')

    def save(self):
        with open(self._config.XML['scriptsPath'], 'w') as f:
            f.write(self._list.pretty_xml())
        try:
            logging.info(
                f'Saved scripts data. Script number: {len(self._list)}'
            )
        except ValueError:
            pass
