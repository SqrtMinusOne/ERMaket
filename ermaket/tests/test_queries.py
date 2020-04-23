import pytest

from ermaket.api.database import DBConn
from ermaket.api.models import Faker
from ermaket.api.queries import (
    ErrorsParser, InsufficientRightsError, QueryBuilder, Transaction
)
from ermaket.api.system.hierarchy import LinkedTableColumn


def _get_sample(db, test_db):
    q = db.query(test_db.model).first()
    obj = q.__marshmallow__().dump(q)

    criterion = {
        "field_name": f"{test_db.model_name}.{test_db.field_name}",
        "operator": "==",
        "field_value": obj[test_db.field_name]
    }
    return obj, criterion


@pytest.mark.usefixtures('test_db')
def test_fetch_many(test_db):
    with DBConn.get_session() as db:
        obj, criterion = _get_sample(db, test_db)

        builder = QueryBuilder(db)
        result = builder.fetch_data(test_db.model, filter_by=[criterion])
        assert len(result) > 0


@pytest.mark.usefixtures('test_db')
def test_fetch_one(test_db):
    with DBConn.get_session() as db:
        obj, criterion = _get_sample(db, test_db)
        builder = QueryBuilder(db)
        found_obj = builder.fetch_one(test_db.model, filter_by=[criterion])
        assert found_obj['_display'] is not None
        del found_obj['_display']
        assert obj == found_obj


@pytest.mark.usefixtures('test_db', 'models')
def test_create(test_db, models):
    model = test_db.model
    entry = test_db.entry

    with DBConn.get_session() as db:
        count = db.query(model).count()

        faker = Faker(models, db=db)
        faked = faker.fake_one(model, db)
        data = faked.__marshmallow__().dump(faked)
        db.rollback()

        transaction = {}
        transaction[entry.id] = {
            'create': {
                'dummy_key': {
                    'newData': data,
                    'links': []
                }
            }
        }

        bad_t = Transaction(db, transaction, role_names=['dummy'])
        with pytest.raises(InsufficientRightsError):
            bad_t.execute()
        assert db.query(model).count() == count

        t = Transaction(db, transaction)
        t.execute()

        assert db.query(model).count() == count + 1


@pytest.mark.usefixtures('test_db')
def test_delete(test_db):
    model = test_db.model
    entry = test_db.entry

    with DBConn.get_session() as db:
        count = db.query(model).count()
        item = db.query(model).first()
        data = model.__marshmallow__().dump(item)
        key = data[entry.pk.rowName]

        transaction = {entry.id: {'delete': {key: True}}}

        bad_t = Transaction(db, transaction, role_names=['dummy'])
        with pytest.raises(InsufficientRightsError):
            bad_t.execute()
        count_after_bad = db.query(model).count()

        t = Transaction(db, transaction)
        t.execute()
        count_after_good = db.query(model).count()
    assert count == count_after_bad
    assert count == count_after_good + 1


@pytest.mark.usefixtures('test_db', 'models')
def test_update(test_db, models):
    model = test_db.model
    entry = test_db.entry
    not_pk = next(
        col for col in entry.columns
        if not col.isPk and not isinstance(col, LinkedTableColumn)
    )

    with DBConn.get_session() as db:
        item = db.query(model).first()
        old_data = model.__marshmallow__().dump(item)
        key = old_data[entry.pk.rowName]

        faker = Faker(models, db=db)
        faked = faker.fake_one(model, db)
        fake_data = faked.__marshmallow__().dump(faked)
        db.rollback()

        new_data = old_data.copy()
        new_data[not_pk.rowName] = fake_data[not_pk.rowName]

        transaction = {
            entry.id:
                {
                    'update': {
                        key: {
                            'newData': new_data,
                            'oldData': old_data
                        }
                    }
                }
        }

        bad_t = Transaction(db, transaction, role_names=['dummy'])
        with pytest.raises(InsufficientRightsError):
            bad_t.execute()
        not_changed_item = db.query(model).filter_by(
            **{
                entry.pk.rowName: key
            }
        ).first()
        assert getattr(not_changed_item,
                       not_pk.rowName) == old_data[not_pk.rowName]

        t = Transaction(db, transaction)
        t.execute()

        changed_item = db.query(model).filter_by(**{
            entry.pk.rowName: key
        }).first()
        assert getattr(changed_item,
                       not_pk.rowName) == new_data[not_pk.rowName]


@pytest.mark.usefixtures('test_db')
def test_exception_handling(test_db):
    entry = test_db.entry
    with DBConn.get_session() as db:
        transaction = {
            entry.id:
                {
                    'create':
                        {
                            'dummy_key':
                                {
                                    'newData':
                                        {
                                            'jackshit': True,
                                            'jackshit2': '12345'
                                        },
                                    'links': []
                                }
                        }
                }
        }

        t = Transaction(db, transaction)
        try:
            t.execute()
        except Exception as exp:
            error, _ = ErrorsParser.parse(exp)
            assert len(error.info) > 0
