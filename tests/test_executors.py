import pytest
import mock
from datetime import (
    datetime,
    timedelta,
)
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


def test_execute_bad_type(dummy_executor):
    command = {'typeXX': 'get', 'url': 'http://1'}
    with pytest.raises(KeyError):
        dummy_executor.execute_command(command)


def test_execute_bad_command(dummy_executor):
    command = {'type': 'get', 'urlXX': 'http://1'}
    with pytest.raises(KeyError):
        dummy_executor.execute_command(command)


def test_execute_not_implemented_command(dummy_executor):
    command = {'type': 'new_command', 'urlXX': 'http://1'}
    dummy_executor.COMMANDS = ['new_command']
    with pytest.raises(NotImplementedError):
        dummy_executor.execute_command(command)


def test_execute_get(dummy_executor):
    command = {'type': 'get', 'url': 'http://1'}
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_click(dummy_executor):
    command = {
        'type': 'clickElement',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        }
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        .click \
        .assert_called_once_with() is None


def test_execute_fill(dummy_executor):
    command = {
        'type': 'setElementText',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        .fill \
        .assert_called_once_with('text value') is None


def test_execute_select_text(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body')
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with('./option[text()="{0}"]'.format('text value'))
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with()


def test_execute_select_value(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'value': '1',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body')
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with('./option[@value="{0}"]'.format('1'))
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with()


def test_execute_select_bad(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'value': '1',
        'text': 'text',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_assert_element_present_default(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_false(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.page.find_element.return_value = None
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_true(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'negated': True,
    }
    dummy_executor.page.find_element.return_value = 1
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_send_keys(dummy_executor):
    from selenium.webdriver.common.keys import Keys
    command = {
        'type': 'sendKeysToElement',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'text': 'ENTER',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .page \
        .find_element \
        .return_value \
        ._element \
        .send_keys \
        .assert_called_once_with(getattr(Keys, 'ENTER'))


def test_execute_send_keys_bad(dummy_executor):
    command = {
        'type': 'sendKeysToElement',
        'locator': {
             'type': 'css selector',
             'value': 'body'
        },
        'text': 'ENTERxxx',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_pause(dummy_executor):
    command = {
        'type': 'pause',
        'waitTime': '1500',
    }
    now = datetime.now()
    dummy_executor.execute_command(command)
    now_now = datetime.now()
    future_date = now + timedelta(milliseconds=1500)
    assert now_now >= future_date


def test_execute_pause_int(dummy_executor):
    command = {
        'type': 'pause',
        'waitTime': 1500,
    }
    now = datetime.now()
    dummy_executor.execute_command(command)
    now_now = datetime.now()
    future_date = now + timedelta(milliseconds=1500)
    assert now_now >= future_date


def test_execute_pause_bad(dummy_executor):
    command = {
        'type': 'pause',
        'waitTime': 'adsf',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_store_eval(dummy_executor):
    command = {
        'type': 'storeEval',
        'variable': 'TAG_NAME',
        'script': 'document.body.tagName',
    }
    assert 'TAG_NAME' not in dummy_executor.variables
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'BODY'

    dummy_executor.execute_command(command)
    assert dummy_executor.variables['TAG_NAME'] == 'BODY'


def test_execute_store_eval_param(dummy_executor):
    command = {
        'type': 'storeEval',
        'variable': 'DYNAMIC',
        'script': '"$foo" + "$foo"',
    }
    assert 'DYNAMIC' not in dummy_executor.variables
    assert 'foo' in dummy_executor.variables
    assert dummy_executor.variables['foo'] == 'bar'

    dummy_executor.execute_command(command)

    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" + "bar"')


def test_execute_verify_eval(dummy_executor):
    command = {
        'type': 'verifyEval',
        'value': 'result',
        'script': '"res" + "ult"',
    }
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'result'

    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"res" + "ult"')


def test_execute_verify_eval_false(dummy_executor):
    command = {
        'type': 'verifyEval',
        'value': 'result',
        'script': '"res" + "ult"',
    }
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'resultXXX'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_execute_verify_eval_param(dummy_executor):
    command = {
        'type': 'verifyEval',
        'value': 'resultbar',
        'script': '"res" + "ult" + "$foo"',
    }
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'resultbar'

    dummy_executor.execute_command(command)
    dummy_executor \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"res" + "ult" + "bar"')


def test_execute_wait_until_condition(dummy_executor):
    command = {
        'type': 'waitUntilCondition',
        'value': 'id1',
        'script': "document.body.getAttribute('id')",
    }

    dummy_executor.execute_command(command)

    dummy_executor \
        .page \
        .wait \
        .until \
        .called
