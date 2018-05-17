# -*- coding: utf-8 -*-
import warnings
import json
import os
import configparser
import re
import pytest
from _pytest.fixtures import FixtureRequest
from collections import namedtuple


def pytest_collect_file(parent, path):
    """ Collect test_XXX.json files """
    if path.ext == ".json" and path.basename.startswith("test_"):
        return JSONFile(path, parent)


class JSONFile(pytest.File):

    def _get_metadata_path(self):
        """ Returns metadata path """
        dirname = self.fspath.dirname
        basename = os.path.splitext(self.fspath.basename)[0]
        ini_file_name = '{0}.ini'.format(basename)
        ini_file_path = os.path.join(dirname, ini_file_name)
        return ini_file_path

    def _get_markers(self, pytest_conf):
        """ Setup markers """
        raw_markers = pytest_conf.get('markers', '')
        markers = [marker for marker in raw_markers.splitlines()
                   if marker]
        return markers

    def _add_markers(self, json_item, markers):
        for marker in markers:
            if self.get_marker(marker) is None:
                if self.config.option.strict:
                    # register marker (strict mode)
                    self.session.config.addinivalue_line(
                        "markers", "{}: {}".format(
                            marker,
                            'dynamic marker'))
            json_item.add_marker(marker)

    def _get_test_data(self, pytest_conf):
        """ Return an array of test data if available """
        raw_test_data = pytest_conf.get('test_data', '')
        test_data = []
        for item in raw_test_data.splitlines():
            if item:
                test_data.append(json.loads(item))
        return test_data

    def collect(self):

        ini_file_path = self._get_metadata_path()
        test_data = []
        markers = []
        if os.path.isfile(ini_file_path):
            # a pytest-play ini file exists for the given item
            config = configparser.ConfigParser()
            config.read(ini_file_path)
            if 'pytest' in config.sections():
                pytest_conf = config['pytest']

                markers = self._get_markers(pytest_conf)
                test_data = self._get_test_data(pytest_conf)
        if not test_data:
            json_item = JSONItem(self.nodeid, self, self.fspath)
            self._add_markers(json_item, markers)
            yield json_item
        else:
            for index, data in enumerate(test_data):
                json_item = JSONItem('{0}{1}'.format(self.nodeid, index),
                                     self,
                                     self.fspath,
                                     test_data=data)
                self._add_markers(json_item, markers)
                yield json_item


class JSONItem(pytest.Item):

    def __init__(self, name, parent, path, test_data=None):
        super(JSONItem, self).__init__(name, parent)
        self.path = getattr(path, 'strpath', path)
        self.fixture_request = None
        self.play_json = None
        self.raw_data = None
        self.test_data = test_data is not None and test_data or {}

    @property
    def module(self):
        """ Needed for Taurus/bzt/BlazeMeter compatibility
            See https://bit.ly/2GE2KS4 """
        return namedtuple(
            re.sub('\W|^(?=\d)', '_', os.path.basename(self.path)),
            [])

    def setup(self):
        self._setup_request()
        self._setup_play()
        self._setup_raw_data()

    def _setup_fixtures(self):
        def func():
            pass

        self.funcargs = {}
        fm = self.session._fixturemanager
        self._fixtureinfo = fm.getfixtureinfo(node=self, func=func,
                                              cls=None, funcargs=False)
        fixture_request = FixtureRequest(self)
        fixture_request._fillfixtures()
        return fixture_request

    def _setup_request(self):
        self.fixture_request = self._setup_fixtures()

    def _setup_play(self):
        self.play_json = self.fixture_request.getfixturevalue('play_json')

    def _setup_raw_data(self):
        self.raw_data = self.play_json.get_file_contents(self.path)

    def runtest(self):
        data = self.play_json.get_file_contents(self.path)
        self.play_json.execute(data, extra_variables=self.test_data)

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
    warnings.warn(
        DeprecationWarning(
            "play_json fixture DEPRECATED, will be removed in version "
            ">=2.0.0). See issue #5"))
    context = bdd_vars.copy()
    if 'pytest-play' in variables:
        for name, value in variables['pytest-play'].items():
            context[name] = value
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
