import csv
import logging
import os
from pathlib import Path

from api.config import Config
from api.database import DBConn

from .models import Models
from .seeder import Seeder

__all__ = ['Dumper']


class Dumper:
    def __init__(self):
        DBConn()
        self._config = Config()
        self._models = Models()
        self._seeder = Seeder(self._models)

    def dump_schema(self, *args, format='csv', **kwargs):
        if format == 'csv':
            with DBConn.get_session() as db:
                return self._dump_csv(*args, db=db, **kwargs)
        raise ValueError(f'Format {format} is unknown')

    def load_schema(self, *args, format='csv', **kwargs):
        if format == 'csv':
            with DBConn.get_session(autoflush=False) as db:
                return self._load_csv(*args, db=db, **kwargs)
        raise ValueError(f'Format {format} is unknown')

    def _dump_csv(self, schema, db, folder=None):
        folder = self._assert_folder(folder)
        for name, model in self._models[schema].items():
            columns = [column.name for column in model.__table__.columns]
            filename = os.path.join(folder, f'{name}.csv')
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)
                for item in db.query(model):
                    writer.writerow(getattr(item, col) for col in columns)
            logging.info(f'Dumped {name} to {filename}')

    def _load_csv(self, schema, db, folder=None):
        folder = self._assert_folder(folder)
        self._seeder.drop_models(schema)
        self._seeder.create_models()
        db.execute('SET CONSTRAINTS ALL DEFERRED')
        for name, model in self._models[schema].items():
            filename = os.path.join(folder, f'{name}.csv')
            with open(filename, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                # db.execute(model.__table__.insert(), list(reader))
                db.bulk_insert_mappings(model, reader)
            logging.info(f'Read {name} from {filename}')
        db.commit()
        logging.info(f'Finished loading {schema}')

    def _assert_folder(self, folder=None):
        if folder is None:
            folder = self._config.Dump['folder']
        Path(folder).mkdir(parents=True, exist_ok=True)
        return folder
