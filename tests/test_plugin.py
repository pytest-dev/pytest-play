# -*- coding: utf-8 -*-


def test_play_engine_class(play_engine_class):
    from pytest_play.engine import PlayEngine
    assert play_engine_class is PlayEngine


def test_play(play):
    assert play.variables['base_url'] == 'http://'
