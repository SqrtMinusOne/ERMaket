import pytest

from api.database import DBConn
from api.queries import QueryBuilder


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
        assert obj == found_obj
