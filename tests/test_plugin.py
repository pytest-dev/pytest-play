# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def browser():
    import mock
    browser = mock.MagicMock()

    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    alsoProvides(browser, ISplinter)
    return browser


def test_play_engine_class(play_engine_class):
    from pytest_play.engine import PlayEngine
    assert play_engine_class is PlayEngine


def test_play_json(play_json, navigation, bdd_vars, parametrizer_class):
    assert play_json.navigation is navigation
    assert play_json.navigation.page is navigation.page
    assert play_json.variables != bdd_vars
    assert 'base_url' in play_json.variables
    assert 'base_url' not in bdd_vars
    assert play_json.parametrizer_class is parametrizer_class


def test_play_json_variables(play_json, navigation, bdd_vars,
                             parametrizer_class):
    """ If you provide values inside a pytest-play section of your pytest-variables
        file, they become available to pytest-play """
    assert 'date_format' in play_json.variables
    assert 'date_formant' not in bdd_vars
    assert play_json.variables['date_format'] == 'YYYYMMDD'
