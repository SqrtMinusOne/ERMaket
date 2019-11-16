from api import Config

import glob
import importlib


__all__ = ['Models']


class Models:
    """A class for managing the SQLAlchemy models directory.
    As models are generated classes, they have to be imported dynamically.

    Models are separated by schemas; schemas can be accessed as this class'
    attributes.

    related config.json parameters: Models
    """

    def __init__(self):
        self.config = Config()
        self.schemas = {}
        self._paths = {}
        self._import()

    def _import(self):
        for filename in glob.glob("{0}/{1}*.py".format(
            self.config.Models['models_dir'],
            self.config.Models['model_prefix']
        )):
            module_name = filename.replace('/', '.')[:-3]
            module = importlib.import_module(module_name)

            for class_name in module.__all__:
                model = getattr(module, class_name)
                schema = model.__table_args__['schema']
                try:
                    self.schemas[schema][class_name] = model
                    self._paths[schema][class_name] = module_name
                except KeyError:
                    self.schemas[schema] = {class_name: model}
                    self._paths[schema] = {class_name: module_name}

    def __getattr__(self, key):
        return self.schemas[key]

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __iter__(self):
        for schema in self.schemas.values():
            for table in schema.values():
                yield table
