#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytest_play` package."""

import pytest


@pytest.fixture(scope='session')
def variables():
    return {'skins': {'skin1': {'base_url': 'http://', 'credentials': {}}}}


@pytest.mark.parametrize('expression', [
    '200 == 200',
    '200 != 404 and 10>0',
    'variables["foo"] == "baz"',
    '"foo" in variables',
    'len([1]) == 1',
    '[1][0] == 1',
    'len(list(variables.items())) == 1',
    'variables["foo"].upper() == "BAZ"',
    'match(r"^([0-9]*)-data", "123-data")',
    'match(r"^([0-9]*)-data", "123-data").group(1) == "123"',
    'datetime.datetime.now() > (datetime.datetime.now() - '
    'datetime.timedelta(seconds=1))'
])
def test_assertion(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
    })


def test_assertion_ko():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(AssertionError):
        provider.command_assert({
            'provider': 'python',
            'type': 'assert',
            'expression': '200 == 404'
        })


@pytest.mark.parametrize('expression', [
    'open("/etc/passwd", "r")',
    'open',
    'import os',
    '__file__',
    '__file__',
    '__builtins__.__dict__["bytes"]',
    '__builtins__.__dict__["bytes"] = "pluto"',
    'prova = lambda: 1',
    'os = 1',
])
def test_assertion_bad(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    with pytest.raises(Exception):
        provider.command_assert({
            'provider': 'python',
            'type': 'assert',
            'expression': expression
        })


def test_store_variable():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_store_variable({
        'provider': 'python',
        'type': 'store_variable',
        'expression': '1+1',
        'name': 'sum2'
    })
    assert 'sum2' in mock_engine.variables
    assert mock_engine.variables['foo'] == 'baz'
    assert mock_engine.variables['sum2'] == 2


def test_exec():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    assert provider.command_exec({
        'provider': 'python',
        'type': 'exec',
        'expression': '1+1',
        }) == 2


@pytest.mark.parametrize('expression', [
    'variable == 200',
])
def test_assertion_kwargs(expression):
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {'foo': 'baz'}
    assert 'variable' not in mock_engine.variables
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
        },
        variable=200)
    assert 'variable' not in mock_engine.variables


def test_sleep():
    import mock
    mock_engine = mock.MagicMock()
    mock_engine.variables = {}
    from pytest_play import providers
    provider = providers.PythonProvider(mock_engine)
    assert provider.engine is mock_engine
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    provider.command_sleep({
        'provider': 'python',
        'type': 'sleep',
        'seconds': 2
    })
    now_now = datetime.now()
    expected_date = now + timedelta(milliseconds=2000)
    assert now_now >= expected_date


def test_wait_until_countdown(play_json):
    play_json.variables = {'countdown': 10}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    play_json.execute_command({
        'provider': 'python',
        'type': 'wait_until',
        'expression': 'variables["countdown"] == 0',
        'timeout': 1.3,
        'poll': 0.1,
        'sub_commands': [{
            'provider': 'python',
            'type': 'store_variable',
            'name': 'countdown',
            'expression': 'variables["countdown"] - 1'
        }]
    })
    now_now = datetime.now()
    expected_date = now + timedelta(seconds=0.9)
    assert now_now >= expected_date


def test_wait_until_countdown_no_poll(play_json):
    play_json.variables = {'countdown': 10}
    play_json.execute_command({
        'provider': 'python',
        'type': 'wait_until',
        'expression': 'variables["countdown"] == 0',
        'timeout': 0,
        'poll': 0,
        'sub_commands': [{
            'provider': 'python',
            'type': 'store_variable',
            'name': 'countdown',
            'expression': 'variables["countdown"] - 1'
        }]
    })


def test_wait_until_countdown_timeout(play_json):
    from pytest_play.providers.python import TimeoutException
    play_json.variables = {'countdown': 20}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    with pytest.raises(TimeoutException):
        play_json.execute_command({
            'provider': 'python',
            'type': 'wait_until',
            'expression': 'variables["countdown"] == 0',
            'timeout': 1.3,
            'poll': 0.1,
            'sub_commands': [{
                'provider': 'python',
                'type': 'store_variable',
                'name': 'countdown',
                'expression': 'variables["countdown"] - 1'
            }]
        })
    now_now = datetime.now()
    expected_date = now + timedelta(seconds=1.3)
    assert now_now >= expected_date


def test_wait_until_not_countdown(play_json):
    play_json.variables = {'countdown': 10}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    play_json.execute_command({
        'provider': 'python',
        'type': 'wait_until_not',
        'expression': 'variables["countdown"] > 0',
        'timeout': 1.3,
        'poll': 0.1,
        'sub_commands': [{
            'provider': 'python',
            'type': 'store_variable',
            'name': 'countdown',
            'expression': 'variables["countdown"] - 1'
        }]
    })
    now_now = datetime.now()
    expected_date = now + timedelta(seconds=0.9)
    assert now_now >= expected_date


def test_wait_until_not_countdown_timeout(play_json):
    from pytest_play.providers.python import TimeoutException
    play_json.variables = {'countdown': 20}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    with pytest.raises(TimeoutException):
        play_json.execute_command({
            'provider': 'python',
            'type': 'wait_until_not',
            'expression': 'variables["countdown"] > 0',
            'timeout': 1.3,
            'poll': 0.1,
            'sub_commands': [{
                'provider': 'python',
                'type': 'store_variable',
                'name': 'countdown',
                'expression': 'variables["countdown"] - 1'
            }]
        })
    now_now = datetime.now()
    expected_date = now + timedelta(seconds=1.3)
    assert now_now >= expected_date


def test_skip_condition(play_json):
    play_json.variables = {'foo': 'baz'}
    play_json.execute_command({
        'provider': 'python',
        'type': 'assert',
        'expression': '200 == 404',
        'skip_condition': '"$foo" == "baz"'
    })


def test_skip_condition_str(play_json):
    play_json.variables = {'foo': 'baz'}
    play_json.execute_command("""{
        "provider": "python",
        "type": "assert",
        "expression": "200 == 404",
        "skip_condition": "'$foo' == 'baz'"
    }""")


def test_skip_condition_false(play_json):
    play_json.variables = {'foo': 'baz'}
    with pytest.raises(AssertionError):
        play_json.execute_command({
            'provider': 'python',
            'type': 'assert',
            'expression': '200 == 404',
            'skip_condition': '"$foo" != "baz"'
        })


def test_parametrization_update(play_json):
    play_json.variables = {'countdown': 2}
    play_json.execute_command({
        "provider": "python",
        "type": "wait_until",
        "expression": "variables['countdown'] == 0",
        "timeout": 10,
        "poll": 0,
        "sub_commands": [
            {
             "provider": "python",
             "type": "store_variable",
             "name": "concatenation",
             "expression": "'$countdown' + variables.get('concatenation', '')",
             "comment": "KO, don't use $countdown in loops"
            },
            {
             "provider": "python",
             "type": "store_variable",
             "name": "sum",
             "expression": "variables.get('sum', 0) + variables['countdown']",
             "comment": "OK, use variables['countdown'] instead"
            },
            {
             "provider": "python",
             "type": "store_variable",
             "name": "countdown",
             "expression": "variables['countdown'] - 1"
            }
            ]
        },
    )
    assert play_json.variables['sum'] == 3
    # with wait until loops you should not use string interpolation
    assert play_json.variables['concatenation'] == '22'
