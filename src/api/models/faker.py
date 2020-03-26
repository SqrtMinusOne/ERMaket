import logging

import sqlalchemy as sa
import tqdm
from mixer.backend.sqlalchemy import Mixer
from sqlalchemy.inspection import inspect

from api.config import Config
from api.database import DBConn

from .models import Models

__all__ = ['Faker']


class ResolveError(Exception):
    pass


class Faker:
    """
    Class for automatic filling the database with test data

    """

    def __init__(self, models: Models, verbose=False, fake=False, db=None):
        self._models = models
        self._config = Config()
        self._verbose = verbose
        self._mixer = None
        self._fake = fake
        self._silence_system_warn = False
        self._max_resolve = 20

        if db:
            self._init_mixer(db)

    def _init_mixer(self, db):
        self._mixer = Mixer(session=db, commit=False, fake=self._fake)

    def fake_all(self, default_num=5):
        """Fill the database with fake data

        :param default_num: number of entries per table
        """
        schemas = list(self._models.schemas.keys())
        if 'system' in schemas:
            self.fake_schema('system', default_num=default_num)
            schemas.remove('system')
            self._silence_system_warn = True
        for schema in schemas:
            self.fake_schema(schema, default_num=default_num)
        self._silence_system_warn = False

    def fake_schema(self, schema, entries={}, default_num=5):
        """Fill the database schema tables with fake data

        raises ResolveError if could not resolve foreign keys

        :param schema: schema name
        :param entries: {model_name: number_of_entries}
        model_name is generated camelCase
        :param default_num: number of entries, if t_name is not in entries
        """
        if 'system' in self._models.schemas and not self._silence_system_warn:
            logging.warning(
                'If the model has references to system tables, '
                'it may be required to fake schema `system` first'
            )
        generated = {name: 0 for name in self._models[schema].keys()}
        not_resolved = {name: 0 for name in self._models[schema].keys()}
        if schema in self._config.Faker['ignore']:
            for key in self._config.Faker['ignore'][schema]:
                del generated[key]
                del not_resolved[key]

        total = sum(
            [
                entries.get(name, default_num)
                for name in self._models[schema].keys()
            ]
        )
        try:
            if self._verbose:
                bar = tqdm.tqdm(total=total)

            with DBConn.get_session(autoflush=False) as db:
                self._init_mixer(db)
                while len(generated) > 0:
                    finished = []
                    for name, i in generated.items():
                        if i >= entries.get(name, default_num):
                            finished.append(name)
                            continue

                        model = self._models[schema][name]
                        if self._fake_model(model, db):
                            generated[name] += 1
                            if self._verbose:
                                bar.update(1)
                            not_resolved[name] = 0
                        else:
                            not_resolved[name] += 1
                            if not_resolved[name] > self._max_resolve:
                                raise ResolveError(
                                    f"Can't resolve foreign keys for {name}"
                                )
                    for name in finished:
                        del generated[name]
                    self._flush_faked(db)

        finally:
            if self._verbose:
                bar.close()

    def fake_one(self, model, db):
        """Generate fake model

        :param model: SQLAlchemy model
        :param db: session, connection or engine
        :returns: model instance, if fks were resolved successfully
        """
        attributes = {}
        resolved = True
        relationships = inspect(model).relationships.values()
        for name, attr in dict(model.__table__.columns).items():
            if attr.foreign_keys:
                fk = next(iter(attr.foreign_keys))
            else:
                continue
            t_name = '.'.join(fk._column_tokens[:-1])
            # backref_name = fk._column_tokens[1]
            column = fk._column_tokens[-1]
            entry = list(
                db.execute(
                    f"SELECT {column} FROM {t_name} ORDER BY RANDOM() LIMIT 1"
                )
            )
            if not entry:
                resolved = False
                break
            else:
                attributes[name] = entry[0][0]
                rel = self._get_relationship(relationships, name)
                if rel:
                    target = self._models[rel.target.schema][rel.argument.arg]
                    search = {}
                    search[column] = entry[0][0]
                    obj = db.query(target).filter_by(**search).first()
                    attributes[rel.class_attribute.key] = obj
        if resolved:
            faked = self._mixer.blend(model, **attributes)
            return faked
        return None

    def _flush_faked(self, db):
        try:
            db.commit()
        except sa.exc.IntegrityError:
            db.rollback()  # TODO logging

    def _fake_model(self, model, db):
        faked = self.fake_one(model, db)
        if faked:
            db.add(faked)
            return True
        return False

    def _get_relationship(self, relationships, column_name):
        for r in relationships:
            if any([
                c.name == column_name
                for c in r.local_columns
            ]):
                return r

    def faked_models(self):
        models = []
        for schema in self._models.schemas.keys():
            if schema not in self._config.Faker['ignore']:
                models.extend(self._models[schema].values())
            else:
                for key, model in self._models[schema].items():
                    if key not in self._config.Faker['ignore'][schema]:
                        models.append(model)
        return models
