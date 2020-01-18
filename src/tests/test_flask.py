import pytest


@pytest.mark.usefixtures("client")
def test_login(client):
    response = client.get('/auth/current')
    print(response)
