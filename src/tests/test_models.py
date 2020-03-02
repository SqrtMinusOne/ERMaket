import pytest

from api.database import DBConn
from api.models import Models


@pytest.mark.usefixtures("config")
def test_connection():
    DBConn.reset()
    with pytest.raises(TypeError):
        DBConn.Session()
    DBConn()
    with DBConn.get_session() as sess:
        assert sess


@pytest.mark.usefixtures("block_singletons")
def test_models():
    models = Models()
    assert len(models.schemas) > 0

    list_ = list(models)
    assert len(list_) > 0

    models2 = Models()
    assert len(models.schemas) == len(models2.schemas)


@pytest.mark.usefixtures("models", "test_db")
def test_marshmallow(models):
    with DBConn.get_session() as db:
        for model in iter(models):
            item = db.query(model).first()
            obj = model.__marshmallow__(session=db).dump(item)
            assert obj is not None
