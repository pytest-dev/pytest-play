import os
import pytest


pytest_plugins = 'pytester'


@pytest.fixture
def data_base_path():
    """ selenium/splinter base path, where json files live """
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'data')


@pytest.fixture(scope='session')
def variables():
    return {
        'pytest-play': {'date_format': 'YYYYMMDD'},
        'skins': {
            'skin1': {
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
def dummy_executor(play):
    play.variables.update(**{'foo': 'bar'})
    assert play.variables['test_run_identifier'].startswith('QA-')
    assert play.variables['date_format'] == 'YYYYMMDD'
    assert play.variables['base_url'] == 'http://'
    assert play.variables['Administrator_name'] == 'admin'
    assert play.variables['Administrator_pwd'] == 'pwd'
    assert play.variables['foo'] == 'bar'
    return play
