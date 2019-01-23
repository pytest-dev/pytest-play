# -*- coding: utf-8 -*-


def test_play_engine_class(play_engine_class):
    from pytest_play.engine import PlayEngine
    assert play_engine_class is PlayEngine


def test_play(play):
    assert play.variables['base_url'] == 'http://'


def test_get_marker():
    import mock
    node = mock.MagicMock()
    node.get_closest_marker.side_effect = AttributeError()
    node.get_marker.return_value = None
    from pytest_play.plugin import get_marker
    assert get_marker(node, 'name') is None
    assert node.get_marker.assert_called_once_with(
        'name') is None
