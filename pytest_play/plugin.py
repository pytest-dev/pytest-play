# -*- coding: utf-8 -*-
import uuid            # pragma: no cover
import yaml            # pragma: no cover
import os              # pragma: no cover
import re              # pragma: no cover
import pytest          # pragma: no cover
from _pytest.fixtures import (    # pragma: no cover
    FixtureRequest,
    FixtureLookupError,
)
from collections import namedtuple  # pragma: no cover


def get_marker(node, name):
    try:
        marker = node.get_closest_marker(name)
    except AttributeError:
        # backwards compatibility with old pytest versions
        marker = node.get_marker(name)
    return marker


def pytest_collect_file(parent, path):
    """ Collect test_XXX.yml files """
    if path.ext in(".yaml", ".yml") and path.basename.startswith("test_"):
        return YAMLFile(path, parent=parent)


class YAMLFile(pytest.File):
    def __init__(self, fspath, parent=None, config=None,
                 session=None, nodeid=None):
        super(YAMLFile, self).__init__(fspath, parent=parent, config=config)
        self.obj = self

    def _get_metadata_path(self):
        """ Returns metadata path """
        dirname = self.fspath.dirname
        basename = os.path.splitext(self.fspath.basename)[0]
        metadata_file_name = '{0}.metadata'.format(basename)
        metadata_file_path = os.path.join(dirname, metadata_file_name)
        return metadata_file_path

    def _get_markers(self, conf):
        """ Setup markers """
        raw_markers = conf.get('markers', [])
        markers = [marker for marker in raw_markers
                   if marker]
        return markers

    def _add_markers(self, yml_item, markers):
        for marker in markers:
            if get_marker(self, marker) is None:
                if self.config.option.strict:
                    # register marker (strict mode)
                    self.session.config.addmetadatavalue_line(
                        "markers", "{}: {}".format(
                            marker,
                            'dynamic marker'))
            yml_item.add_marker(marker)

    def _get_test_data(self, conf):
        """ Return an array of test data if available """
        return conf.get('test_data', '')

    def collect(self):

        metadata_file_path = self._get_metadata_path()
        test_data = []
        markers = []
        if os.path.isfile(metadata_file_path):
            # a pytest-play metadata file exists for the given item
            with open(metadata_file_path) as metadata_file:
                config = yaml.safe_load(metadata_file)

                markers = self._get_markers(config)
                test_data = self._get_test_data(config)
        if not test_data:
            yml_item = YAMLItem(self.nodeid, parent=self, config=self.config)
            self._add_markers(yml_item, markers)
            yield yml_item
        else:
            for index, data in enumerate(test_data):
                yml_item = YAMLItem('{0}{1}'.format(self.nodeid, index),
                                    parent=self,
                                    config=self.config,
                                    test_data=data)
                self._add_markers(yml_item, markers)
                yield yml_item


class YAMLItem(pytest.Item):
    def __init__(self, name, parent=None, config=None, session=None,
                 nodeid=None, test_data=None):
        super(YAMLItem, self).__init__(
            name, parent, config, session, nodeid=nodeid)
        self.path = getattr(parent.fspath, 'strpath')
        self.fixture_request = None
        self.play = None
        self.raw_data = None
        self.test_data = test_data is not None and test_data or {}

    @property
    def module(self):
        """ Needed for Taurus/bzt/BlazeMeter compatibility
            See https://bit.ly/2GE2KS4 """
        return namedtuple(
            re.sub(r'\W|^(?=\d)', '_', os.path.basename(self.path)),
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
        self.play = self.fixture_request.getfixturevalue('play')

    def _setup_raw_data(self):
        self.raw_data = self.play.get_file_contents(self.path)

    def runtest(self):
        data = self.play.get_file_contents(self.path)
        self.play.execute_raw(data, extra_variables=self.test_data)


@pytest.fixture
def play_engine_class():
    """ Play engine class  class """
    from .engine import PlayEngine
    return PlayEngine


@pytest.fixture
def play(request, play_engine_class, variables):
    """
        How to use yml_executor::

            def test_experimental(play):
                data = play.get_file_contents(
                    '/my/path/etc', 'login.yml')
                play.execute_raw(data)
    """
    context = None
    skin = None
    try:
        bdd_vars = request.getfixturevalue('bdd_vars')
        context = bdd_vars.copy()
        skin = request.getfixturevalue('skin')
    except FixtureLookupError:
        context = context is not None and context or {
            'test_run_identifier': "QA-{0}".format(str(uuid.uuid1()))}
        skin = skin is not None and skin or 'skin1'

    if 'pytest-play' in variables:
        for name, value in variables['pytest-play'].items():
            context[name] = value
    if 'skins' in variables and skin is not None:
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
    play = play_engine_class(request, context)
    yield play
    play.teardown()
