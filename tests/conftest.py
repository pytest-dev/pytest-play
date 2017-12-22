import os
import pytest
import mock


pytest_plugins = 'pytester'


@pytest.fixture
def data_base_path():
    """ selenium/splinter base path, where json files live """
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'data')


@pytest.fixture(scope='session')
def variables(skin):
    return {
        'skins': {
            skin: {
                'base_url': 'http://',
                'credentials': {
                    'Administrator': {
                        'username': 'admin',
                        'password': 'pwd'
                    }
                }
            }
        }
    }


@pytest.fixture
def dummy_executor(parametrizer_class, navigation):
    from pytest_play.engine import PlayEngine
    return PlayEngine(navigation, {'foo': 'bar'}, parametrizer_class)


@pytest.fixture
def page_instance():
    return mock.MagicMock()


@pytest.fixture(autouse=True)
def included_scenario(play_json, data_getter, data_base_path):
    data = data_getter(data_base_path, 'included-scenario.json')
    play_json.register_steps(
        data, 'included-scenario.json')
