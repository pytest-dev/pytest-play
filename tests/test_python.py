#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytest_play` package."""

import pytest


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
def test_assertion(expression, play):
    play.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
    })


def test_assertion_ko(play):
    play.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
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
def test_assertion_bad(expression, play):
    play.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    with pytest.raises(Exception):
        provider.command_assert({
            'provider': 'python',
            'type': 'assert',
            'expression': expression
        })


def test_store_variable(play):
    play.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    provider.command_store_variable({
        'provider': 'python',
        'type': 'store_variable',
        'expression': '1+1',
        'name': 'sum2'
    })
    assert 'sum2' in play.variables
    assert play.variables['foo'] == 'baz'
    assert play.variables['sum2'] == 2


def test_exec(play):
    play.variables = {'foo': 'baz'}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    assert provider.command_exec({
        'provider': 'python',
        'type': 'exec',
        'expression': '1+1',
        }) == 2


@pytest.mark.parametrize('expression', [
    'variable == 200',
])
def test_assertion_kwargs(expression, play):
    play.variables = {'foo': 'baz'}
    assert 'variable' not in play.variables
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    provider.command_assert({
        'provider': 'python',
        'type': 'assert',
        'expression': expression
        },
        variable=200)
    assert 'variable' not in play.variables


def test_sleep(play):
    play.variables = {}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
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


@pytest.mark.parametrize("sleep_time", [0.1, "0.1"])
def test_sleep_float(sleep_time, play):
    play.variables = {}
    from pytest_play import providers
    provider = providers.PythonProvider(play)
    provider.command_sleep({
        'provider': 'python',
        'type': 'sleep',
        'seconds': sleep_time
    })


def test_wait_until_countdown(play):
    play.variables = {'countdown': 10}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    play.execute_command({
        'provider': 'python',
        'type': 'wait_until',
        'expression': 'variables["countdown"] == 0',
        'timeout': 2.3,
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


def test_wait_until_countdown_no_poll(play):
    play.variables = {'countdown': 10}
    play.execute_command({
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


def test_wait_until_no_sub_commands(play):
    play.variables = {'countdown': 0}
    play.execute_command({
        'provider': 'python',
        'type': 'wait_until',
        'expression': 'variables["countdown"] == 0',
        'timeout': 0,
        'poll': 0,
    })


def test_wait_until_not_no_sub_commands(play):
    play.variables = {'countdown': 10}
    play.execute_command({
        'provider': 'python',
        'type': 'wait_until_not',
        'expression': 'variables["countdown"] == 0',
        'timeout': 0,
        'poll': 0,
    })


def test_wait_until_countdown_timeout(play):
    from pytest_play.providers.python import TimeoutException
    play.variables = {'countdown': 20}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    with pytest.raises(TimeoutException):
        play.execute_command({
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


def test_wait_until_not_countdown(play):
    play.variables = {'countdown': 10}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    play.execute_command({
        'provider': 'python',
        'type': 'wait_until_not',
        'expression': 'variables["countdown"] > 0',
        'timeout': 2.3,
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


def test_wait_until_not_countdown_timeout(play):
    from pytest_play.providers.python import TimeoutException
    play.variables = {'countdown': 20}
    from datetime import (
        datetime,
        timedelta,
    )
    now = datetime.now()
    with pytest.raises(TimeoutException):
        play.execute_command({
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


def test_skip_condition(play):
    play.variables = {'foo': 'baz'}
    play.execute_command({
        'provider': 'python',
        'type': 'assert',
        'expression': '200 == 404',
        'skip_condition': '"$foo" == "baz"'
    })


def test_skip_condition_false(play):
    play.variables = {'foo': 'baz'}
    with pytest.raises(AssertionError):
        play.execute_command({
            'provider': 'python',
            'type': 'assert',
            'expression': '200 == 404',
            'skip_condition': '"$foo" != "baz"'
        })


def test_parametrization_update(play):
    play.variables = {'countdown': 2}
    play.execute_command({
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
        }
    )
    assert play.variables['sum'] == 3
    # with wait until loops you should not use string interpolation
    assert play.variables['concatenation'] == '22'


def test_parametrization_update_non_string(play):
    import yaml
    play.variables = {'sleep_time': 0.5}
    # should not raise any exception
    play.execute_command(yaml.load("""
---
provider: python
type: sleep
seconds: $sleep_time
    """))


def test_parametrization_template_string(play):
    play.variables = {}
    # should not raise any exception
    play.execute_raw("""
---
- provider: python
  type: store_variable
  name: sleep_time
  expression: "0.5"
- provider: python
  type: sleep
  seconds: $sleep_time
        """)


def test_parametrization_template_string_2(play):
    play.variables = {}
    # should not raise any exception
    play.execute_raw("""
---
- provider: python
  type: store_variable
  name: python
  expression: '{"comment": "a default comment"}'
- provider: python
  type: sleep
  seconds: "0.1"
  comment: a default comment
        """)
