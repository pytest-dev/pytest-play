# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def bdd_vars():
    """ Simulate integration with play_selenium """
    return {'using': 'bdd_vars'}


def test_play_variables(play, bdd_vars):
    """ If you provide values inside a pytest-play section of your pytest-variables
        file, they become available to pytest-play """
    assert 'date_format' in play.variables
    assert 'date_format' not in bdd_vars
    assert play.variables['date_format'] == 'YYYYMMDD'
    assert play.variables['using'] == 'bdd_vars'
