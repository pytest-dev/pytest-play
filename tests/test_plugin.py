# -*- coding: utf-8 -*-
import os
import pytest
from pytest_play.executors import JSONExecutorSplinter


@pytest.fixture
def browser():
    import mock
    browser = mock.MagicMock()

    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    alsoProvides(browser, ISplinter)
    return browser


@pytest.fixture
def data_base_path():
    """ selenium/splinter base path, where json files live """
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'data')


def test_executor_splinter_class(json_executor_splinter_class):
    assert json_executor_splinter_class is JSONExecutorSplinter


def test_data_getter(data_base_path, data_getter):
    contents = data_getter(data_base_path, 'login.json')
    assert '$base_url' in contents


def test_default_executor(default_json_executor_class):
    assert default_json_executor_class is JSONExecutorSplinter


def test_play_json(play_json, navigation, bdd_vars, parametrizer_class):
    assert play_json.navigation is navigation
    assert play_json.navigation.page is navigation.page
    assert play_json.variables != bdd_vars
    assert 'base_url' in play_json.variables
    assert 'base_url' not in bdd_vars
    assert play_json.parametrizer_class is parametrizer_class
