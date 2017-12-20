import pytest
import mock
from datetime import (
    datetime,
    timedelta,
)


def test_play_engine_constructor(bdd_vars, parametrizer_class):
    from pytest_play.engine import PlayEngine
    executor = PlayEngine(None, bdd_vars, parametrizer_class)
    assert executor.parametrizer_class is parametrizer_class
    assert executor.navigation is None
    assert executor.variables == bdd_vars


def test_splinter_executor_parametrizer(dummy_executor):
    assert dummy_executor.parametrizer.parametrize('$foo') == 'bar'


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


def test_execute_condition_true(dummy_executor):
    command = {'type': 'get',
               'url': 'http://1',
               'condition': '"$foo" === "bar"'}
    dummy_executor.navigation.page.driver.evaluate_script.return_value = True
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" === "bar"') is None
    dummy_executor \
        .navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_condition_false(dummy_executor):
    command = {'type': 'get',
               'url': 'http://1',
               'condition': '"$foo" === "bar1"'}
    dummy_executor.navigation.page.driver.evaluate_script.return_value = False
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" === "bar1"') is None
    dummy_executor \
        .navigation \
        .page \
        .driver_adapter \
        .open \
        .called is False


def test_execute_get(dummy_executor):
    command = {'type': 'get', 'url': 'http://1'}
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_get_basestring(dummy_executor):
    command = """{"type": "get", "url": "http://1"}"""
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with('http://1') is None


def test_execute_get_basestring_param(dummy_executor):
    command = """{"type": "get", "url": "http://$foo"}"""
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with('http://bar') is None


def test_execute_click(dummy_executor):
    command = {
        'type': 'clickElement',
        'locator': {
             'type': 'css',
             'value': 'body'
        }
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .click \
        .assert_called_once_with() is None
    assert dummy_executor.navigation.page.wait.until.called is True


def test_execute_fill(dummy_executor):
    command = {
        'type': 'setElementText',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .fill \
        .assert_called_once_with('text value') is None


def test_execute_select_text(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with(
            './option[text()="{0}"]'.format('text value')) is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with() is None


def test_execute_select_value(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'value': '1',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with(
            './option[@value="{0}"]'.format('1')) is None
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with() is None


def test_execute_select_bad(dummy_executor):
    command = {
        'type': 'select',
        'locator': {
             'type': 'css',
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
             'type': 'css',
             'value': 'body'
        },
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_false(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.navigation.page.find_element.return_value = None
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_true(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': True,
    }
    dummy_executor.navigation.page.find_element.return_value = 1
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_default(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }
    dummy_executor.navigation.page.find_element.return_value.visible = True
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.navigation.page.find_element.return_value.visible = True
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated_false(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.navigation.page.find_element.return_value.visible = False
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated_true(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': True,
    }
    dummy_executor.navigation.page.find_element.return_value.visible = True
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_send_keys(dummy_executor):
    from selenium.webdriver.common.keys import Keys
    command = {
        'type': 'sendKeysToElement',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'ENTER',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        .navigation \
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
             'type': 'css',
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
        .navigation \
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
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" + "bar"')


def test_execute_eval(dummy_executor):
    command = {
        'type': 'eval',
        'script': '"$foo" + "$foo"',
    }
    assert dummy_executor.variables['foo'] == 'bar'

    dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
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
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'result'

    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
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
        .navigation \
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
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'resultbar'

    dummy_executor.execute_command(command)
    dummy_executor \
        .navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"res" + "ult" + "bar"')


def test_execute_wait_until_condition(dummy_executor):
    command = {
        'type': 'waitUntilCondition',
        'script': "document.body.getAttribute('id')",
    }

    dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .wait \
        .until \
        .called


def test_execute_wait_for_element_present(dummy_executor):
    command = {
        'type': 'waitForElementPresent',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }

    def _until(func):
        func(dummy_executor.navigation.page.driver)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .visible = True
    dummy_executor \
        .navigation \
        .page \
        .wait \
        .until \
        .side_effect = _until

    dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .wait \
        .until \
        .called
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_wait_for_element_visible(dummy_executor):
    command = {
        'type': 'waitForElementVisible',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }

    def _until(func):
        func(dummy_executor.navigation.page.driver)

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .visible = True
    dummy_executor \
        .navigation \
        .page \
        .wait \
        .until \
        .side_effect = _until

    dummy_executor.execute_command(command)

    dummy_executor \
        .navigation \
        .page \
        .wait \
        .until \
        .called
    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_verify_text_default(dummy_executor):
    command = {
        'type': 'verifyText',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
    }

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    dummy_executor.execute_command(command)


def test_execute_verify_text(dummy_executor):
    command = {
        'type': 'verifyText',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
        'negated': False
    }

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    dummy_executor.execute_command(command)


def test_execute_verify_text_negated(dummy_executor):
    command = {
        'type': 'verifyText',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
        'negated': True
    }

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_execute_verify_text_false(dummy_executor):
    command = {
        'type': 'verifyText',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
    }

    dummy_executor \
        .navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is another text!'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_new_provider_custom_command(dummy_executor):
    command = {'type': 'newCommand', 'provider': 'newprovider'}
    dummy_provider = mock.MagicMock()

    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)
    dummy_executor.register_command_provider(
        dummy_provider, 'newprovider')

    # execute new custom command
    dummy_executor.execute_command(command)

    assert dummy_provider.assert_called_once_with(dummy_executor) is None
    assert dummy_provider \
        .return_value \
        .command_newCommand \
        .assert_called_once_with(command)
