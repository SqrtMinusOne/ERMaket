import os

from api.config import Config
from api.system.hierarchy import Hierachy

__all__ = ['HierachyManager']

_hierarchy = None


class HierachyManager:
    def __init__(self, reload=False):
        self._config = Config()
        self.read(reload)

    def read(self, reload):
        global _hierarchy
        if _hierarchy is None or reload:
            if os.path.exists(self._config.XML['hierarchyPath']):
                with open(self._config.XML['hierarchyPath']) as f:
                    _hierarchy = Hierachy.from_xml(f.read())
            else:
                _hierarchy = Hierachy()
        self.hierarchy = _hierarchy

    def save(self):
        with open(self._config.XML['hierarchyPath'], 'w') as f:
            f.write(self.hierarchy.pretty_xml())

    def __del__(self):
        self.save()
