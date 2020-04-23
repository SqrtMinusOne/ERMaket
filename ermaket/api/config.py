import json
import os

from ermaket.utils import Singleton, get_project_root

__all__ = ['Config']

_configs = {}


class Config(metaclass=Singleton):
    """configs JSON wrapper"""
    configs = {}

    def __init__(self, reload=False):
        self.read(reload)

    def __getattr__(self, key: str):
        return self.configs[key]

    def read(self, reload):
        global _configs
        if len(_configs) == 0 or reload:
            with open(
                os.path.join(get_project_root(), './config/config.json')
            ) as f:
                _configs = json.load(f)
        self.configs = _configs
        self.update_paths()

    def update_paths(self):
        for path in self.FileRoot:
            attr_path = path.split('.')
            self._set_absolute_path(attr_path[1:], getattr(self, attr_path[0]))

    def _set_absolute_path(self, attr_path, obj):
        if len(attr_path) > 1:
            return self._set_absolute_path(attr_path[1:], obj[attr_path[0]])
        else:
            obj[attr_path[0]] = os.path.normpath(
                os.path.join(get_project_root(), obj[attr_path[0]])
            )

    def __str__(self):
        return str(self.configs)
