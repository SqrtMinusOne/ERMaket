import pytest

from api.database import DBConn
from api.models import Dumper


@pytest.mark.usefixtures('test_db')
def test_dump(test_db):
    dumper = Dumper()
    seeder = dumper._seeder

    model = test_db.model

    with DBConn.get_session() as db:
        count_before = db.query(model).count()
        assert count_before > 0

    dumper.dump_schema(test_db.schema)
    seeder.drop_models(test_db.schema)
    seeder.create_models()

    with DBConn.get_session() as db:
        assert db.query(model).count() == 0

    dumper.load_schema(test_db.schema)

    with DBConn.get_session() as db:
        assert db.query(model).count() == count_before
