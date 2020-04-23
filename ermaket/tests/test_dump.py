import pytest

from ermaket.api.database import DBConn
from ermaket.api.models import Dumper


@pytest.mark.usefixtures('test_db')
def test_dump(test_db):
    dumper = Dumper()
    seeder = dumper._seeder

    model = test_db.model

    with DBConn.get_session() as db:
        count_before = db.query(model).count()
    assert count_before > 0

    dumper.dump_schema(test_db.schema)
    dumper.dump_schema('system')
    seeder.drop_models()
    seeder.create_models()

    with DBConn.get_session() as db:
        count_empty = db.query(model).count()
    assert count_empty == 0

    dumper.load_schema('system')
    dumper.load_schema(test_db.schema)

    with DBConn.get_session() as db:
        count_after = db.query(model).count()
    assert count_after == count_before
