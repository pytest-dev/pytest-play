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
def browser():
    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    driver = mock.MagicMock()
    alsoProvides(driver, ISplinter)
    return driver


@pytest.fixture
def page_instance(browser):
    return mock.MagicMock()


@pytest.fixture
def dummy_executor(parametrizer_class, navigation, page_instance):
    from pytest_play.engine import PlayEngine
    engine = PlayEngine(navigation, {'foo': 'bar'}, parametrizer_class)
    # initialize browser
    engine.navigation.setPage(page_instance)
    engine.navigation.get_page_instance = lambda *args, **kwargs: page_instance
    return engine


@pytest.fixture(autouse=True)
def included_scenario(play_json, data_getter, data_base_path):
    data = data_getter(data_base_path, 'included-scenario.json')
    play_json.register_steps(
        data, 'included-scenario.json')
