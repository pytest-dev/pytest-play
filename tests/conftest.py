import pytest
import mock


pytest_plugins = 'pytester'


@pytest.fixture(scope='session')
def variables(skin):
    return {'skins': {skin: {'base_url': 'http://',
                             'credentials': {}}}}


@pytest.fixture
def dummy_executor(parametrizer_class, navigation):
    from pytest_play.engine import PlayEngine
    return PlayEngine(navigation, {'foo': 'bar'}, parametrizer_class)


@pytest.fixture
def page_instance():
    return mock.MagicMock()
