# -*- coding: utf-8 -*-
import pytest
from _pytest.fixtures import FixtureRequest


def _setup_fixtures(json_item):
    def func():
        pass

    json_item.funcargs = {}
    fm = json_item.session._fixturemanager
    json_item._fixtureinfo = fm.getfixtureinfo(node=json_item, func=func,
                                               cls=None, funcargs=False)
    fixture_request = FixtureRequest(json_item)
    fixture_request._fillfixtures()
    return fixture_request


def pytest_collect_file(parent, path):
    if path.ext == ".json" and path.basename.startswith("test_"):
        return JSONFile(path, parent)


class JSONFile(pytest.File):

    def collect(self):
        yield JSONItem(self.nodeid, self, self.fspath)


class JSONItem(pytest.Item):
    def __init__(self, name, parent, path):
        super(JSONItem, self).__init__(name, parent)
        self.path = path
        self.fixture_request = None
        self.play_json = None

    def setup(self):
        self.fixture_request = _setup_fixtures(self)
        self.play_json = self.fixture_request.getfixturevalue('play_json')

    def runtest(self):
        data = self.play_json.get_file_contents(self.path)
        self.play_json.execute(data)

    def repr_failure(self, excinfo):
        """ called when self.runtest() raises an exception. """
        if isinstance(excinfo.value, JSONException):
            return "\n".join([
                "usecase execution failed",
                "   spec failed: %r: %r" % excinfo.value.args[1:3],
                "   no further details known at this point."
            ])

    def reportinfo(self):
        return self.fspath, 0, "usecase: %s" % self.name


class JSONException(Exception):
    """ custom exception for error reporting. """


@pytest.fixture
def play_engine_class():
    """ Play engine class  class """
    from .engine import PlayEngine
    return PlayEngine


@pytest.fixture
def play_json(request, play_engine_class, bdd_vars, variables, skin):
    """
        How to use json_executor::

            def test_experimental(play_json):
                data = play_json.get_file_contents(
                    '/my/path/etc', 'login.json')
                play_json.execute(data)
    """
    context = bdd_vars.copy()
    if 'skins' in variables:
        skin_settings = variables['skins'][skin]
        if 'base_url' in skin_settings:
            context['base_url'] = skin_settings['base_url']
        if 'credentials' in skin_settings:
            for credential_name, credential_settings in \
                    skin_settings['credentials'].items():
                username_key = "{0}_name".format(credential_name)
                password_key = "{0}_pwd".format(credential_name)
                context[username_key] = credential_settings['username']
                context[password_key] = credential_settings['password']
    play_json = play_engine_class(request, context)
    yield play_json
    play_json.teardown()
