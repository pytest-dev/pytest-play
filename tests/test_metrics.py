#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytest_play` package."""
import pytest


def test_record_elapsed():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    mock_record_property = mock.MagicMock()
    mock_record_property_statsd = mock.MagicMock()
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    provider._record_property = mock_record_property
    provider._record_property_statsd = mock_record_property_statsd
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
    assert mock_record_property \
        .assert_called_once_with(
            'previous_command', elapsed) is None
    assert mock_record_property_statsd \
        .assert_called_once_with(
            'previous_command', elapsed, metric_type='timing',
            meas_unit='s') is None


def test_record_elapsed_statsd():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    mock_record_property = mock.MagicMock()
    from pytest_play import providers
    with mock.patch(
            'pytest_play.providers.metrics.MetricsProvider.statsd_client',
            new_callable=mock.PropertyMock) as statsd_client:
        provider = providers.MetricsProvider(mock_engine)
        provider._record_property = mock_record_property
        assert provider.engine is mock_engine
        provider.command_record_elapsed({
            'provider': 'metrics',
            'type': 'record_elapsed',
            'name': 'previous_command',
            'comment': 'record last command elapsed time '
            'under key name previous command'
        })
        assert statsd_client.return_value.timing.assert_called_once() is None


def test_record_elapsed_key_error():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(KeyError):
        provider.command_record_elapsed({
            'provider': 'metrics',
            'type': 'record_elapsed',
            'name': 'previous_command',
            'comment': 'record last command elapsed time '
            'under key name previous command'
        })


def test_record_property():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    mock_record_property = mock.MagicMock()
    mock_record_property_statsd = mock.MagicMock()
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    provider._record_property = mock_record_property
    provider._record_property_statsd = mock_record_property_statsd
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
    assert mock_record_property \
        .assert_called_once_with(
            'elapsed_milliseconds', elapsed*1000) is None
    assert mock_record_property_statsd \
        .assert_called_once_with(
            'elapsed_milliseconds', elapsed*1000,
            metric_type=None, meas_unit=None) is None


@pytest.mark.xfail
def test_record_property_statsd():
    import mock
    mock_engine = mock.MagicMock()
    elapsed = 0.125
    mock_engine.variables = {'_elapsed': elapsed}
    mock_record_property = mock.MagicMock()
    from pytest_play import providers
    with mock.patch(
            'pytest_play.providers.metrics.MetricsProvider.statsd_client',
            new_callable=mock.PropertyMock) as statsd_client:
        provider = providers.MetricsProvider(mock_engine)
        provider._record_property = mock_record_property
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
        assert mock_record_property \
            .assert_called_once_with(
                'elapsed_milliseconds', elapsed*1000) is None
        assert statsd_client.return_value.timing \
            .assert_called_once_with(
                'elapsed_milliseconds', elapsed*1000) is None


def test_record_elapsed_start():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    time_start = 1550770816.1716287
    with mock.patch('pytest_play.providers.metrics.time') as time:
        time.time.return_value = time_start
        provider.command_record_elapsed_start({
            'provider': 'metrics',
            'type': 'record_elapsed_start',
            'name': 'async_update',
        })
    assert mock_engine.update_variables.assert_called_once_with(
        {'async_update': time_start}) is None


def test_record_elapsed_stop():
    import mock
    mock_engine = mock.MagicMock()
    time_start = 1550770816.1716287
    mock_engine.variables = {'async_update': time_start}
    mock_record_property = mock.MagicMock()
    mock_record_property_statsd = mock.MagicMock()
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    provider._record_property = mock_record_property
    provider._record_property_statsd = mock_record_property_statsd
    assert provider.engine is mock_engine
    time_stop = 1550770817.1716287
    with mock.patch('pytest_play.providers.metrics.time') as time:
        time.time.return_value = time_stop
        provider.command_record_elapsed_stop({
            'provider': 'metrics',
            'type': 'record_elapsed_stop',
            'name': 'async_update',
        })
    assert mock_engine.update_variables.assert_called_once_with(
        {'async_update': time_stop-time_start}) is None


def test_record_elapsed_stop_statsd():
    import mock
    mock_engine = mock.MagicMock()
    time_start = 1550770816.1716287
    mock_engine.variables = {'async_update': time_start}
    mock_record_property = mock.MagicMock()
    from pytest_play import providers
    with mock.patch(
            'pytest_play.providers.metrics.MetricsProvider.statsd_client',
            new_callable=mock.PropertyMock) as statsd_client:
        provider = providers.MetricsProvider(mock_engine)
        provider._record_property = mock_record_property
        assert provider.engine is mock_engine
        time_stop = 1550770817.1716287
        with mock.patch('pytest_play.providers.metrics.time') as time:
            time.time.return_value = time_stop
            provider.command_record_elapsed_stop({
                'provider': 'metrics',
                'type': 'record_elapsed_stop',
                'name': 'async_update',
            })
        assert statsd_client.return_value.timing.assert_called_once_with(
            'async_update', (time_stop-time_start)*1000) is None


def test_record_elapsed_stop_key_error():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {}
    from pytest_play import providers
    provider = providers.MetricsProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(KeyError):
        provider.command_record_elapsed_stop({
            'provider': 'metrics',
            'type': 'record_elapsed_stop',
            'name': 'async_update',
        })
