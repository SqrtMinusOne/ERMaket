import os
import shutil

from jinja2 import Environment, FileSystemLoader

from api.config import Config
from api.models import NamesConverter

from .types import erd_to_sqla_type

__all__ = ['Generator']


class Generator:
    def __init__(self, tables, schema):
        self._config = Config()
        self._env = Environment(loader=FileSystemLoader(
            self._config.Generation['templates_folder']))
        self._env.globals['Names'] = NamesConverter
        self._env.globals['sa_type'] = erd_to_sqla_type
        # self._env.trim_blocks = True
        self._env.lstrip_blocks = True
        self._template = self._env.get_template('model.tmpl.py')

        self._tables = tables
        self._schema = schema

    def _generate_model(self, name):
        render = self._template.render(schema=self._schema,
                                       table=self._tables[name])
        return render

    def generate_models(self, folder):
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        for name, table in self._tables.items():
            with open(os.path.join(folder, f"{name}.py"), 'w') as f:
                f.write(self._generate_model(name))
