import logging
import os
from fnmatch import fnmatch

from api.config import Config
from api.system.hierarchy import Activation
from utils.xml import RootMixin, xmllist, xmltuple

__all__ = ['Script', 'ScriptList', 'Activations']

Activations = xmllist('Activations', 'activations', Activation)

Script = xmltuple(
    'Script',
    'script', ['path', 'activations'], [Activations],
    kws=['id'],
    types={'id': int}
)

_ScriptList = xmllist('ScriptList', 'scripts', Script)


class ScriptList(_ScriptList, RootMixin):
    def __init__(self, xml=None, scripts=None):
        self._config = Config()
        args, kwargs = self._init_root(
            xml,
            self._config.XML["ScriptListAttributes"],
            values=scripts,
        )
        super().__init__(*args, **kwargs)

    @classmethod
    def discover(cls):
        scripts = []
        config = Config()
        for subdir, dirs, files in os.walk(config.Scripts['folder']):
            for f in files:
                if fnmatch(f, f"{config.Scripts['prefix']}*.py"):
                    scripts.append(os.path.join(subdir, f))
        logging.info(f'Discovered scripts: {len(scripts)}')
        return cls(
            scripts=[Script(path=f, id=i) for i, f in enumerate(scripts)]
        )
