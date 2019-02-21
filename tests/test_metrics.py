#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytest_play` package."""


def test_record_property_elapsed():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_record_property({
        'provider': 'metrics',
        'name': 'previous_command',
        'comment': 'record last command elapsed time '
        'under key name previous command'
    })
    assert mock_engine \
        .update_variables \
        .assert_called_once_with(
            {'previous_command': elapsed}) is None
    assert mock_engine \
        .record_property \
        .assert_called_once_with(
            'previous_command', elapsed) is None
