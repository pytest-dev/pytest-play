# -*- coding: utf-8 -*-
import re
from time import sleep
from selenium.webdriver.common.keys import Keys


class JSONExecutorSplinter(object):

    COMMANDS = [
        'get',
        'waitForElementPresent',
        'setElementText',
        'clickElement',
        'assertElementPresent',
        'sendKeysToElement',
        'pause',
        'verifyText',
        'storeEval',
        'verifyEval',
        'waitUntilCondition',
        'select',
        'verifyElementPresent',
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

    def __init__(self, page, variables, parametrizer_class):
        self.page = page
        self.variables = variables
        self.parametrizer_class = parametrizer_class

    @property
    def parametrizer(self):
        """ Parametrizer engine """
        return self.parametrizer_class(self.variables)

    def _locator(self, locator):
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
        elif command_type == 'assertElementPresent':
            method_name = command_prefix.format('assert_element_present')
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
        elif command_type == 'waitUntilCondition':
            method_name = command_prefix.format('wait_until_condition')
        elif command_type == 'select':
            method_name = command_prefix.format('select')
        elif command_type == 'verifyElementPresent':
            method_name = command_prefix.format('verify_element_present')
        else:
            raise NotImplementedError(
                'Command not implemented', command_type)
        getattr(self, method_name)(command)

    # commands
    def command_get(self, command):
        """ get """
        self.page.driver_adapter.open(command['url'])

    def command_click(self, command):
        """ clickElement """
        self.command_wait_for_element_present(command)

        selector = self._locator(command['locator'])
        self.page.find_element(*selector).click()

    def command_fill(self, command):
        """ setElementText """
        self.command_wait_for_element_present(command)

        selector = self._locator(command['locator'])
        text = command['text']
        self.page.find_element(*selector).fill(text)

    def command_select(self, command):
        """ select """
        self.command_wait_for_element_present(command)

        selector = self._locator(command['locator'])

        text = command.get('text', None)
        value = command.get('value', None)
        if text is not None and value is not None:
            raise ValueError('You cannot specify both text and value')

        raw_element = self.page.find_element(*selector)._element
        raw_element.click()
        if text is not None:
            option = raw_element.find_element_by_xpath(
                './option[text()="{0}"]'.format(text))
        else:
            option = raw_element.find_element_by_xpath(
                './option[@value="{0}"]'.format(value))
        option.click()

    def command_wait_for_element_present(self, command):
        """ waitForElementPresent """
        selector = self._locator(command['locator'])

        def _wait(driver):
            element = self.page.find_element(*selector)
            return element is not None and element.visible
        self.page.wait.until(_wait)

    def command_assert_element_present(self, command):
        """ assertElementPresent """
        selector = self._locator(command['locator'])
        negated = command['negated']
        element = self.page.find_element(*selector)
        assert not negated and element

    def command_send_keys_to_element(self, command):
        """ send_keys_to_element """
        self.command_wait_for_element_present(command)

        key = command['text']
        if key not in self.KEYS:
            raise ValueError('Key not allowed', key)

        selector = self._locator(command['locator'])
        self.page.find_element(*selector) \
            ._element \
            .send_keys(getattr(Keys, key))

    def command_pause(self, command):
        """ pause """
        wait_time = float(command['waitTime'])
        sleep(wait_time/1000.0)

    def command_verify_text(self, command):
        """ verifyText """
        self.command_wait_for_element_present(command)

        selector = self._locator(command['locator'])
        negated = command['negated']
        pattern = self.parametrizer.parametrize(command['text'])
        element = self.page.find_element(*selector)
        match = re.search(pattern, element.text)
        assert not negated and match

    def command_store_eval(self, command):
        """ storeEval """
        variable = command['variable']
        script = self.parametrizer.parametrize(command['script'])
        value = self.page.driver.evaluate_script(script)
        self.variables[variable] = value

    def command_verify_eval(self, command):
        """ verifyEval """
        value = command['value']
        script = self.parametrizer.parametrize(command['script'])
        assert value == self.page.driver.evaluate_script(script)

    def command_wait_until_condition(self, command):
        """ waitUntilCondition  """
        value = command['value']
        script = self.parametrizer.parametrize(command['script'])
        self.page.wait.until(
            lambda s: self.page.driver.evaluate_script(script) == value)

    def command_verify_element_present(self, command):
        """ assertElementPresent """
        selector = self._locator(command['locator'])
        negated = command['negated']
        element = self.page.find_element(*selector)
        assert negated and not element or element
