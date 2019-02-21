#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytest_play` package."""


def test_record_elapsed():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_record_elapsed({
        'provider': 'metrics',
        'type': 'record_elapsed',
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


def test_record_property():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    mock_engine.execute_command.return_value = elapsed*1000
    provider.command_record_property({
        'provider': 'metrics',
        'type': 'record_property',
        'name': 'elapsed_milliseconds',
        'expression': 'variables["_elapsed"]*1000',
    })
    assert mock_engine.execute_command.assert_called_once_with(
        {'provider': 'python',
         'type': 'exec',
         'expression': 'variables["_elapsed"]*1000'}) is None
    assert mock_engine \
        .update_variables \
        .assert_called_once_with(
            {'elapsed_milliseconds': elapsed*1000}) is None
    assert mock_engine \
        .record_property \
        .assert_called_once_with(
            'elapsed_milliseconds', elapsed*1000) is None
