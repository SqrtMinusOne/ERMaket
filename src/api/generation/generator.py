import glob
import logging
import os

from jinja2 import Environment, FileSystemLoader
from yapf.yapflib.yapf_api import FormatCode

from api.config import Config
from api.models import NamesConverter

from .types import erd_to_sqla_type

__all__ = ['Generator']


class Generator:
    def __init__(self, tables, schema):
        self._config = Config()
        self._env = Environment(
            loader=FileSystemLoader(
                self._config.Generation['templates_folder']
            )
        )
        self._env.globals['Names'] = NamesConverter
        self._env.globals['sa_type'] = erd_to_sqla_type
        # self._env.trim_blocks = True
        self._env.lstrip_blocks = True
        self._template = self._env.get_template('model.tmpl.py')

        self._tables = tables
        self._schema = schema

    def _generate_model(self, name):
        render = self._template.render(
            schema=self._schema, table=self._tables[name]
        )
        return self._postprocess_python(render)

    def _postprocess_python(self, code):
        # while re.search('\n\n\n', code):
        #     code = re.sub('\n\n\n', '\n\n', code)
        code, _ = FormatCode(code, style_config='facebook')
        return code

    def generate_models(self):
        files = {}
        for name, table in self._tables.items():
            files[name] = self._generate_model(name)
        return files

    def clear_folder(self, folder=None, prefix=None, schema=None):
        if folder is None:
            folder = self._config.Models['models_dir']
        if prefix is None:
            prefix = self._config.Models['model_prefix']
        path = f"{folder}/{prefix}"
        if schema:
            path += schema
        path += '*'
        for f in glob.glob(path):
            os.remove(f)
            logging.info(f'Removed file: {f}')

    def generate_folder(self, folder=None, prefix=None):
        if folder is None:
            folder = self._config.Models['models_dir']
        if prefix is None:
            prefix = self._config.Models['model_prefix']
        self.clear_folder(folder, prefix, self._schema)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        for name, table in self._tables.items():
            filename = f"{prefix}{self._schema}_{name}.py"
            path = os.path.join(folder, filename)
            with open(path, 'w') as f:
                f.write(self._generate_model(name))
                logging.info(f'Created file {path}')
        base_name = os.path.join(folder, "base.py")
        with open(base_name, 'w') as f:
            f.write(self._env.get_template('base.tmpl.py').render())
            logging.info(f'Created file {base_name}')
