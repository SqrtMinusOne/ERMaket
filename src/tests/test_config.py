import pytest


@pytest.mark.usefixtures("config")
def test_config(config):
    assert hasattr(config, 'Database')


@pytest.mark.usefixtures("config")
def test_reload1(config):
    config.Database['host'] = '1234'
    assert config.Database['user'] != 'test'


@pytest.mark.usefixtures("config")
def test_reload2(config):
    assert config.Database['host'] != '1234'
    config.Database['user'] = 'test'
