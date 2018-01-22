import re
from time import sleep
from selenium.webdriver.common.keys import Keys
from . import BaseProvider
import warnings


warnings.warn(
    "This provider will be moved to a separate package in 2.0.0",
    DeprecationWarning)


class SplinterCommandProvider(BaseProvider):
    """ JSON executor """

    SELECTOR_TYPES = [
        'css',
        'xpath',
        'tag',
        'name',
        'text',
        'id',
        'value',
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

    def locator_translate(self, locator):
        """ Translates json locator to splinter selector
            format
        """
        selector = locator['value']
        locator_type = locator['type']

        if locator_type not in self.SELECTOR_TYPES:
            raise ValueError('Not allowed selector type')

        return (locator_type, selector,)

    # decorators
    def wait_for_element_visible(func):
        """ Wait for element present decorator and
            wait for element visible) """
        def wrapper(*args):
            command = args[1]
            args[0].command_waitForElementVisible(command)
            return func(*args)
        return wrapper

    def condition(func):
        """ Skip command if condition script returns False """
        def wrapper(*args):
            command = args[1]
            condition = command.get('condition', None)
            skip = False
            if condition is not None:
                expr = args[0].engine.parametrizer.parametrize(condition)
                if not args[0].engine.navigation.page.driver.evaluate_script(
                        expr):
                    skip = True
            if not skip:
                return func(*args)
        return wrapper

    # commands
    @condition
    def command_get(self, command, **kwargs):
        """ get """
        if self.engine.navigation.page is None:
            page = self.engine.navigation.get_page_instance()
            self.engine.navigation.setPage(page)
        self.engine.navigation.page.driver_adapter.open(command['url'])

    @wait_for_element_visible
    @condition
    def command_clickElement(self, command, **kwargs):
        """ clickElement """
        selector = self.locator_translate(command['locator'])
        self.engine.navigation.page.find_element(*selector).click()

    @wait_for_element_visible
    @condition
    def command_setElementText(self, command, **kwargs):
        """ setElementText """
        selector = self.locator_translate(command['locator'])
        text = command['text']
        self.engine.navigation.page.find_element(*selector).fill(text)

    @wait_for_element_visible
    @condition
    def command_select(self, command, **kwargs):
        """ select """
        selector = self.locator_translate(command['locator'])

        text = command.get('text', None)
        value = command.get('value', None)
        if text is not None and value is not None:
            raise ValueError('You cannot specify both text and value')

        raw_element = self.engine.navigation.page.find_element(
            *selector)._element
        raw_element.click()
        if text is not None:
            option = raw_element.find_element_by_xpath(
                './option[text()="{0}"]'.format(text))
        else:
            option = raw_element.find_element_by_xpath(
                './option[@value="{0}"]'.format(value))
        option.click()

    @condition
    def command_waitForElementPresent(self, command, **kwargs):
        """ waitForElementPresent """
        selector = self.locator_translate(command['locator'])

        def _wait(driver):
            element = self.engine.navigation.page.find_element(*selector)
            return element is not None
        self.engine.navigation.page.wait.until(_wait)

    @condition
    def command_waitForElementVisible(self, command, **kwargs):
        """ waitForElementVisible """
        selector = self.locator_translate(command['locator'])

        def _wait(driver):
            element = self.engine.navigation.page.find_element(*selector)
            return element is not None and element.visible
        self.engine.navigation.page.wait.until(_wait)

    @condition
    def command_assertElementPresent(self, command, **kwargs):
        """ assertElementPresent """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        element = self.engine.navigation.page.find_element(*selector)
        result = False
        if negated:
            result = not element
        else:
            result = element
        assert result

    @condition
    def command_assertElementVisible(self, command, **kwargs):
        """ assertElementVisible """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        element = self.engine.navigation.page.find_element(*selector)
        result = False
        if negated:
            result = not element.visible
        else:
            result = element.visible
        assert result

    @wait_for_element_visible
    @condition
    def command_sendKeysToElement(self, command, **kwargs):
        """ sendKeysToElement """
        key = command['text']
        if key not in self.KEYS:
            raise ValueError('Key not allowed', key)

        selector = self.locator_translate(command['locator'])
        self.engine.navigation.page.find_element(*selector) \
            ._element \
            .send_keys(getattr(Keys, key))

    @condition
    def command_pause(self, command, **kwargs):
        """ pause """
        wait_time = float(command['waitTime'])
        sleep(wait_time/1000.0)

    @wait_for_element_visible
    @condition
    def command_verifyText(self, command, **kwargs):
        """ verifyText """
        selector = self.locator_translate(command['locator'])
        negated = command.get('negated', False)
        pattern = self.engine.parametrizer.parametrize(command['text'])
        element = self.engine.navigation.page.find_element(*selector)
        match = re.search(pattern, element.text)
        assert not negated and match

    @condition
    def command_storeEval(self, command, **kwargs):
        """ storeEval """
        variable = command['variable']
        script = self.engine.parametrizer.parametrize(command['script'])
        value = self.engine.navigation.page.driver.evaluate_script(script)
        self.engine.variables[variable] = value

    @condition
    def command_verifyEval(self, command, **kwargs):
        """ verifyEval """
        value = command['value']
        script = self.engine.parametrizer.parametrize(command['script'])
        assert value == self.engine.navigation.page.driver.evaluate_script(
            script)

    @condition
    def command_eval(self, command, **kwargs):
        """ eval """
        script = self.engine.parametrizer.parametrize(command['script'])
        self.engine.navigation.page.driver.evaluate_script(script)

    @condition
    def command_waitUntilCondition(self, command, **kwargs):
        """ waitUntilCondition  """
        script = self.engine.parametrizer.parametrize(command['script'])
        self.engine.navigation.page.wait.until(
            lambda s: self.engine.navigation.page.driver.evaluate_script(
                script))
