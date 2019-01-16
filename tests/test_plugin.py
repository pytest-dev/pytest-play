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


def test_play(play, navigation, bdd_vars):
    assert play.navigation is navigation
    assert play.navigation.page is navigation.page
    assert play.variables != bdd_vars
    assert 'base_url' in play.variables
    assert 'base_url' not in bdd_vars


def test_play_variables(play, navigation, bdd_vars):
    """ If you provide values inside a pytest-play section of your pytest-variables
        file, they become available to pytest-play """
    assert 'date_format' in play.variables
    assert 'date_formant' not in bdd_vars
    assert play.variables['date_format'] == 'YYYYMMDD'
