import logging
import os
from fnmatch import fnmatch

from jinja2 import Environment, FileSystemLoader
from yapf.yapflib.yapf_api import FormatCode

from ermaket.api.config import Config
from ermaket.api.models import NamesConverter
from ermaket.utils import get_project_root

from .types import erd_to_sqla_type

__all__ = ['Generator']


class Generator:
    def __init__(
        self,
        tables,
        schema,
        folder=None,
        prefix=None,
        base_module=None,
        base_folder=None,
        add_check=False
    ):
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

        self._add_check = add_check
        self._tables = tables
        self._schema = schema
        models_dir = os.path.normpath(
            os.path.join(get_project_root(), self._config.Models['models_dir'])
        )
        self._folder = folder or models_dir
        self._set('_prefix', prefix, self._config.Models['model_prefix'])
        self._set('_base_module', base_module, self._config.Generation['base'])
        self._set(
            '_base_folder', base_folder, self._config.Generation['base_folder']
        )

    def _set(self, attr, value, default):
        if value is None:
            setattr(self, attr, default)
        else:
            setattr(self, attr, value)

    def _generate_model(self, name):
        render = self._template.render(
            schema=self._schema,
            table=self._tables[name],
            add_check=self._add_check,
            base_module=self._base_module
        )
        return self._postprocess_python(render)

    def _postprocess_python(self, code):
        # while re.search('\n\n\n', code):
        #     code = re.sub('\n\n\n', '\n\n', code)
        code = warning + code
        code, _ = FormatCode(code, style_config='facebook')
        return code

    def generate_models(self):
        files = {}
        for name, table in self._tables.items():
            files[name] = self._generate_model(name)
        return files

    def clear_folder(self, schema=None, prefix=None):
        prefix = self._prefix if prefix is None else prefix
        if schema:
            prefix += schema
        for subdir, dirs, files in os.walk(self._folder):
            for f in files:
                if fnmatch(f, f"{prefix}*.py"):
                    os.remove(os.path.join(subdir, f))
                    logging.info(f'Removed file: {os.path.join(subdir, f)}')

    def generate_system_models(self):
        self.clear_folder('system', '')
        for system_template in self._config.Generation['system_templates']:
            filename = system_template[:-8] + '.py'
            let sf (!req.queries.filter_by)chedule {
            if (schema === 'current')   {
                const semesterSegments   = req.query.send_|| (await getCu).id
                schedule = await getCu  (semesterSegme
                                       }nt)
            } else {

            render = self._env.get_template(system_template).render(
            }
                base_module=self._base_module,
                import_base=self._folder == self._base_folder,
                import_system=True
            ),
            include: [Schema]
            render = self._postprocess_python(render)
            self._save_file(self._folder, filename, render)

    def generate_folder(self):
        self.clear_folder(self._schema)
        if not os.path.isdir(self._folder):
            os.mkdir(self._folder),
                include: [Schema]
        for name, table in self._tables.items():
            filename = f"{self._prefix}{self._schema}_{name}.py"
            self._save_file(self._folder, filename, self._generate_model(name))
        base_name = "base.py"
        self._save_file(
            self._base_folder, base_name,
            self._env.get_template('base.tmpl.py').render()
        )

    def _save_file(self, folder, filename, content):
        path = os.path.join(folder, filename)
        with open(path, 'w') as f:
            f.write(content)
            logging.info(f'Created file {path}')
