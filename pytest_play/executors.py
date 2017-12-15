# -*- coding: utf-8 -*-
import re
from time import sleep
from selenium.webdriver.common.keys import Keys
from pypom_navigation.parametrizer import Parametrizer


class JSONExecutorSplinter(object):
    """ JSON executor """

    COMMANDS = [
        'get',
        'waitForElementPresent',
        'waitForElementVisible',
        'setElementText',
        'clickElement',
        'assertElementPresent',
        'assertElementVisible',
        'sendKeysToElement',
        'pause',
        'verifyText',
        'storeEval',
        'verifyEval',
        'waitUntilCondition',
        'select',
        'eval',
    ]
    SELECTOR_TYPES = [
        'css selector',
    ]
    KEYS = [
        'ADD', 'ALT', 'ARROW_DOWN', 'ARROW_LEFT', 'ARROW_RIGHT',
        'ARROW_UP', 'BACKSPACE', 'BACK_SPACE', 'CANCEL', 'CLEAR',
        'COMMAND', 'CONTROL', 'DECIMAL', 'DELETE', 'DIVIDE',
        'DOWN', 'END', 'ENTER', 'EQUALS', 'ESCAPE', 'F1', 'F10',
        'F11', 'F12', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
        'F9', 'HELP', 'HOME', 'INSERT', 'LEFT', 'LEFT_ALT',
        'LEFT_CONTROL', 'LEFT_SHIFT', 'META', 'MULTIPLY',
        'NULL', 'NUMPAD0', 'NUMPAD1', 'NUMPAD2', 'NUMPAD3',
        'NUMPAD4', 'NUMPAD5', 'NUMPAD6', 'NUMPAD7', 'NUMPAD8',
        'NUMPAD9', 'PAGE_DOWN', 'PAGE_UP', 'PAUSE', 'RETURN',
        'RIGHT', 'SEMICOLON', 'SEPARATOR', 'SHIFT', 'SPACE',
        'SUBTRACT', 'TAB', 'UP',
    ]

    def __init__(self, navigation, variables, parametrizer_class=None):
        self.navigation = navigation
        self.variables = variables
        self.parametrizer_class = parametrizer_class and \
            parametrizer_class or Parametrizer

    @property
    def parametrizer(self):
        """ Parametrizer engine """
        return self.parametrizer_class(self.variables)

    def locator_translate(self, locator):
        """ Translates json locator to splinter selector
            format
        """
        selector = locator['value']
        locator_type = locator['type']
        selector_type = None

        if locator_type not in self.SELECTOR_TYPES:
            raise ValueError('Not allowed selector type')

        if locator_type == 'css selector':
            selector_type = 'css'
        # TODO: add more conditions for supported locator types

        return (selector_type, selector,)

    def execute(self, json_data):
        """ Execute parsed json-like file contents """
        steps = json_data['steps']
        for step in steps:
            self.execute_command(step)

    def execute_command(self, command):
        """ Execute single command """
        command_type = command['type']

        if command_type not in self.COMMANDS:
            raise ValueError('Command not supported', command_type)

        command_prefix = 'command_{0}'
        if command_type == 'get':
            method_name = command_prefix.format('get')
        elif command_type == 'clickElement':
            method_name = command_prefix.format('click')
        elif command_type == 'setElementText':
            method_name = command_prefix.format('fill')
        elif command_type == 'waitForElementPresent':
            method_name = command_prefix.format('wait_for_element_present')
        elif command_type == 'waitForElementVisible':
            method_name = command_prefix.format('wait_for_element_visible')
        elif command_type == 'assertElementPresent':
            method_name = command_prefix.format('assert_element_present')
        elif command_type == 'assertElementVisible':
            method_name = command_prefix.format('assert_element_visible')
        elif command_type == 'sendKeysToElement':
            method_name = command_prefix.format('send_keys_to_element')
        elif command_type == 'pause':
            method_name = command_prefix.format('pause')
        elif command_type == 'verifyText':
            method_name = command_prefix.format('verify_text')
        elif command_type == 'storeEval':
            method_name = command_prefix.format('store_eval')
        elif command_type == 'verifyEval':
            method_name = command_prefix.format('verify_eval')
        elif command_type == 'eval':
            method_name = command_prefix.format('eval')
        elif command_type == 'waitUntilCondition':
            method_name = command_prefix.format('wait_until_condition')
        elif command_type == 'select':
            method_name = command_prefix.format('select')
        else:
            raise NotImplementedError(
                'Command not implemented', command_type)
        getattr(self, method_name)(command)

    # decorators
    def wait_for_element_present(func):
        """ Wait for element present decorator and
            wait for element visible) """
        def wrapper(*args):
            command = args[1]
            args[0].command_wait_for_element_present(command)
            return func(*args)
        return wrapper

    def condition(func):
        """ Skip command if condition script returns False """
        def wrapper(*args):
            command = args[1]
            condition = command.get('condition', None)
            skip = False
            if condition is not None:
                expr = args[0].parametrizer.parametrize(condition)
                if not args[0].navigation.page.driver.evaluate_script(expr):
                    skip = True
            if not skip:
                return func(*args)
        return wrapper

    # commands
    @condition
    def command_get(self, command):
        """ get """
        self.navigation.page.driver_adapter.open(command['url'])

    @wait_for_element_present
    @condition
    def command_click(self, command):
        """ clickElement """
        selector = self.locator_translate(command['locator'])
        self.navigation.page.find_element(*selector).click()

    @wait_for_element_present
    @condition
    def command_fill(self, command):
        """ setElementText """
        selector = self.locator_translate(command['locator'])
        text = command['text']
        self.navigation.page.find_element(*selector).fill(text)

    @wait_for_element_present
    @condition
    def command_select(self, command):
        """ select """
        selector = self.locator_translate(command['locator'])

        text = command.get('text', None)
        value = command.get('value', None)
        if text is not None and value is not None:
            raise ValueError('You cannot specify both text and value')

        raw_element = self.navigation.page.find_element(*selector)._element
        raw_element.click()
        if text is not None:
            option = raw_element.find_element_by_xpath(
                './option[text()="{0}"]'.format(text))
        else:
            option = raw_element.find_element_by_xpath(
                './option[@value="{0}"]'.format(value))
        option.click()

    @condition
    def command_wait_for_element_present(self, command):
        """ waitForElementPresent """
        selector = self.locator_translate(command['locator'])

        def _wait(driver):
            element = self.navigation.page.find_element(*selector)
            return element is not None
        self.navigation.page.wait.until(_wait)

    @condition
    def command_wait_for_element_visible(self, command):
        """ waitForElementVisible """
        selector = self.locator_translate(command['locator'])

        def _wait(driver):
            element = self.navigation.page.find_element(*selector)
            return element is not None and element.visible
        self.navigation.page.wait.until(_wait)

    @condition
    def command_assert_element_present(self, command):
        """ assertElementPresent """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        element = self.navigation.page.find_element(*selector)
        result = False
        if negated:
            result = not element
        else:
            result = element
        assert result

    @condition
    def command_assert_element_visible(self, command):
        """ assertElementVisible """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        element = self.navigation.page.find_element(*selector)
        result = False
        if negated:
            result = not element.visible
        else:
            result = element.visible
        assert result

    @wait_for_element_present
    @condition
    def command_send_keys_to_element(self, command):
        """ sendKeysToElement """
        key = command['text']
        if key not in self.KEYS:
            raise ValueError('Key not allowed', key)

        selector = self.locator_translate(command['locator'])
        self.navigation.page.find_element(*selector) \
            ._element \
            .send_keys(getattr(Keys, key))

    @condition
    def command_pause(self, command):
        """ pause """
        wait_time = float(command['waitTime'])
        sleep(wait_time/1000.0)

    @wait_for_element_present
    @condition
    def command_verify_text(self, command):
        """ verifyText """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        pattern = self.parametrizer.parametrize(command['text'])
        element = self.navigation.page.find_element(*selector)
        match = re.search(pattern, element.text)
        assert not negated and match

    @condition
    def command_store_eval(self, command):
        """ storeEval """
        variable = command['variable']
        script = self.parametrizer.parametrize(command['script'])
        value = self.navigation.page.driver.evaluate_script(script)
        self.variables[variable] = value

    @condition
    def command_verify_eval(self, command):
        """ verifyEval """
        value = command['value']
        script = self.parametrizer.parametrize(command['script'])
        assert value == self.navigation.page.driver.evaluate_script(script)

    @condition
    def command_eval(self, command):
        """ eval """
        script = self.parametrizer.parametrize(command['script'])
        self.navigation.page.driver.evaluate_script(script)

    @condition
    def command_wait_until_condition(self, command):
        """ waitUntilCondition  """
        script = self.parametrizer.parametrize(command['script'])
        self.navigation.page.wait.until(
            lambda s: self.navigation.page.driver.evaluate_script(script))
