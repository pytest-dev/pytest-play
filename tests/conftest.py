import pytest


pytest_plugins = 'pytester'


@pytest.fixture(scope='session')
def variables(skin):
    return {'skins': {skin: {'base_url': 'http://',
                             'credentials': {}}}}
