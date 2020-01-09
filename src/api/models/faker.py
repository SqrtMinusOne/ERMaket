import sqlalchemy as sa
import tqdm
from mixer.backend.sqlalchemy import Mixer

from api.database import DBConn

from .models import Models

__all__ = ['Faker']


class ResolveError(Exception):
    pass


class Faker:
    """
    Class for automatic filling the database with test data

    """
    def __init__(self, models: Models, verbose=False, fake=False):
        self._models = models
        self._verbose = verbose
        self._mixer = None
        self._fake = fake

    def _init_mixer(self, db):
        self._mixer = Mixer(session=db, commit=False, fake=self._fake)

    def fake_all(self, default_num=5):
        """Fill the database with fake data

        :param default_num: number of entries per table
        """
        for schema in self._models.schemas.keys():
            self.fake_schema(schema, default_num=default_num)

    def fake_schema(self, schema, entries={}, default_num=5):
        """Fill the database schema tables with fake data

        raises ResolveError if could not resolve foreign keys

        :param schema: schema name
        :param entries: {model_name: number_of_entries}
        model_name is generated camelCase
        :param default_num: number of entries, if table_name is not in entries
        """
        generated = {name: 0 for name in self._models[schema].keys()}
        not_resolved = {name: 0 for name in self._models[schema].keys()}

        total = sum(
            [
                entries.get(name, default_num)
                for name in self._models[schema].keys()
            ]
        )
        try:
            if self._verbose:
                bar = tqdm.tqdm(total=total)

            with DBConn.get_session() as db:
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
                        else:
                            not_resolved[name] += 1
                            if not_resolved[name] > 3:
                                raise ResolveError(
                                    f"Can't resolve foreign keys for {name}"
                                )
                    for name in finished:
                        del generated[name]
                    self._flush_faked(db)

        finally:
            if self._verbose:
                bar.close()

    def _flush_faked(self, db):
        try:
            db.commit()
        except sa.exc.IntegrityError:
            db.rollback()  # TODO logging

    def _fake_model(self, model, db):
        """Generate fake model

        :param model: SQLAlchemy model
        :param db: session, connection or engine
        :returns: True, if foreign_keys were resolved successfully
        """
        attributes = {}
        resolved = True
        for name, attr in dict(model.__table__.columns).items():
            if attr.foreign_keys:
                fk = next(iter(attr.foreign_keys))
            else:
                continue
            table_name = '.'.join(fk._column_tokens[:-1])
            # backref_name = fk._column_tokens[1]
            column = fk._column_tokens[-1]
            entry = list(
                db.execute(
                    f"SELECT {column} FROM {table_name} ORDER BY RANDOM() LIMIT 1"
                )
            )
            if not entry:
                resolved = False
                break
            else:
                attributes[name] = entry[0][0]
                self._flush_faked(db)
                # attributes[backref_name] = \
                #     self._mixer.SELECT(**{column: entry[0][0]})
        if resolved:
            faked = self._mixer.blend(model, **attributes)
            db.add(faked)
        return resolved
