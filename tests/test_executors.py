import pytest
import mock
from pytest_play.executors import JSONExecutorSplinter


@pytest.fixture
def page():
    return mock.MagicMock()


@pytest.fixture
def dummy_executor(parametrizer_class, page):
    return JSONExecutorSplinter(page, {'foo': 'bar'}, parametrizer_class)


def test_splinter_executor_constructor(bdd_vars, parametrizer_class):
    executor = JSONExecutorSplinter(None, bdd_vars, parametrizer_class)
    assert executor.parametrizer_class is parametrizer_class
    assert executor.page is None
    assert executor.variables == bdd_vars


def test_splinter_executor_parametrizer(dummy_executor):
    assert dummy_executor.parametrizer.parametrize('$foo') == 'bar'


def test_splinter_executor_locator(dummy_executor):
    assert dummy_executor.locator_translate(
        {'type': 'css selector',
         'value': 'body'}) == ('css', 'body')


def test_splinter_executor_locator_bad(dummy_executor):
    with pytest.raises(ValueError):
        dummy_executor.locator_translate(
            {'type': 'css selectorXX',
             'value': 'body'}) == ('css', 'body')


def test_splinter_execute(dummy_executor):
    execute_command_mock = mock.MagicMock()
    dummy_executor.execute_command = execute_command_mock

    json_data = {
        'steps': [
            {'type': 'get', 'url': 'http://1'},
            {'type': 'get', 'url': 'http://2'}
        ]
    }
    dummy_executor.execute(json_data)

    calls = [
        mock.call(json_data['steps'][0]),
        mock.call(json_data['steps'][1]),
    ]
    assert dummy_executor.execute_command.assert_has_calls(
        calls, any_order=False) is None
