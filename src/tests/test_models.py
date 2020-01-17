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


def test_models():
    models = Models()
    assert len(models.schemas) > 0

    list_ = list(models)
    assert len(list_) > 0

    models2 = Models()
    assert len(models.schemas) == len(models2.schemas)


@pytest.mark.usefixtures("models")
def test_marshmallow(models):
    for model in iter(models):
        assert hasattr(model, '__marshmallow__')
