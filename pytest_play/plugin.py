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
from pytest_play.config import (
    STATSD,
    PYTEST_STATSD,
)


def pytest_addoption(parser):
    """
    :param parser:
    :return:
    """

    if STATSD is True:
        if not PYTEST_STATSD:
            group = parser.getgroup('terminal reporting')
            group.addoption(
                '--stats-d', action='store_true',
                help='send test results to graphite')
            group.addoption(
                '--stats-host', action='store', dest='stats_host',
                metavar='host', default='localhost',
                help='statsd host. default is \'localhost\'')
            group.addoption(
                '--stats-port', action='store', dest='stats_port',
                metavar='port', default=8125,
                help='statsd port. default is 8125')
            group.addoption(
                '--stats-prefix', action='store', dest='stats_prefix',
                metavar='prefix', default=None,
                help='prefix to give all stats')


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

    def collect(self):

        test_data = []
        markers = []
        metadata = None
        with open(self.fspath, 'r') as yaml_file:
            documents = list(yaml.safe_load_all(yaml_file))
            len_documents = len(documents)
            assert len_documents <= 2
            if len_documents > 1:
                metadata = documents[0]
        if metadata:
            # a pytest-play metadata exists for the given item
            markers = [marker for marker in metadata.get(
                'markers', []) if marker]
            test_data = metadata.get('test_data', None)
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
        self.raw_data = self.play and self.play.get_file_contents(
            self.path)

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
