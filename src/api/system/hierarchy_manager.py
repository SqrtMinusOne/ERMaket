import atexit
import logging
import os

from api.config import Config
from api.system.hierarchy import Hierachy
from utils import Singleton

__all__ = ['HierachyManager']

_hierarchy = None


class HierachyManager(metaclass=Singleton):
    def __init__(self, reload=False, save=True):
        self._config = Config()
        self.read(reload)
        if save:
            atexit.register(lambda manager: manager.save(), self)

    @property
    def h(self):
        return self.hierarchy

    def read(self, reload):
        global _hierarchy
        if _hierarchy is None or reload:
            if os.path.exists(self._config.XML['hierarchyPath']):
                with open(self._config.XML['hierarchyPath']) as f:
                    _hierarchy = Hierachy.from_xml(f.read())
                logging.info(
                    f'Read hierarchy. Elements number: {len(_hierarchy)}'
                )
            else:
                _hierarchy = Hierachy()
                logging.info(f'Created new hierarchy')
        self.hierarchy = _hierarchy

    def save(self):
        with open(self._config.XML['hierarchyPath'], 'w') as f:
            f.write(self.hierarchy.pretty_xml())
        try:
            logging.info(
                f'Saved hierarchy. Elements number: {len(self.hierarchy)}'
            )
        except ValueError:
            pass

    def drop(self):
        global _hierarchy
        _hierarchy = Hierachy()
        self.hierarchy = _hierarchy
