import os
import pytest


pytest_plugins = 'pytester'


@pytest.fixture
def data_base_path():
    """ selenium/splinter base path, where json files live """
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'data')


@pytest.fixture(scope='session')
def variables(skin):
    return {
        'pytest-play': {'date_format': 'YYYYMMDD'},
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
def dummy_executor(request):
    from pytest_play.engine import PlayEngine
    engine = PlayEngine(request, {'foo': 'bar'})
    return engine
