import logging
from time import (
    sleep,
    time,
)
from RestrictedPython import RestrictionCapableEval
from pytest_play.providers import BaseProvider


logger = logging.getLogger(__name__)


class TimeoutException(Exception):
    """ Timeout exception """


class PythonProvider(BaseProvider):
    """ Python command provider """

    def _get_context(self, extra_context):
        context = self.engine.context
        context.update(extra_context)
        return context

    def command_assert(self, command, **kwargs):
        """ Make an assertion based on a command containing
            a python expression
        """
        expression = command['expression']
        context = self._get_context(kwargs)
        try:
            assert self._exec(
                expression,
                context,
            )
        except Exception as e:
            msg = "FAILED expression: '{0}' (exception: {1})".format(
                expression,
                repr(e))
            logger.error(msg)
            print(msg)
            raise e

    def command_store_variable(self, command, **kwargs):
        """ Store a variable based on a command containing a
            python expression
        """
        expression = command['expression']
        name = command['name']
        context = self._get_context(kwargs)
        self.engine.variables[name] = self._exec(
            expression,
            context,
        )

    def command_exec(self, command, **kwargs):
        """ Exec and return an expression
        """
        expression = command['expression']
        context = self._get_context(kwargs)
        return self._exec(
            expression,
            context,
        )

    def command_sleep(self, command, **kwargs):
        """ Exec and return an expression
        """
        wait_time = float(command['seconds'])
        sleep(wait_time)

    def command_while(self, command, **kwargs):
        """ While expression is true-ish
        """
        timeout = command.get('timeout', 10)
        poll = command.get('poll', 0.1)
        expression = command['expression']
        sub_commands = command.get('sub_commands', [])

        end_time = time() + timeout
        while self.engine.execute_command({
                'provider': 'python',
                'type': 'exec',
                'expression': expression,
                }):
            for sub_cmd in sub_commands:
                self.engine.execute_command(sub_cmd)
            if timeout:
                if time() > end_time:
                    raise TimeoutException(command, timeout)
            if poll:
                sleep(poll)

    def command_wait_until(self, command, **kwargs):
        """ Wait until an expression is not False
        """
        timeout = command.get('timeout', 10)
        poll = command.get('poll', 0.1)
        expression = command['expression']
        sub_commands = command.get('sub_commands', [])

        end_time = time() + timeout
        while True:
            for sub_cmd in sub_commands:
                self.engine.execute_command(sub_cmd)
            if self.engine.execute_command({
                    'provider': 'python',
                    'type': 'exec',
                    'expression': expression,
                    }):
                return
            if timeout:
                if time() > end_time:
                    break
            if poll:
                sleep(poll)
        raise TimeoutException(command, timeout)

    def command_wait_until_not(self, command, **kwargs):
        """ Wait until an expression is False
        """
        timeout = command.get('timeout', 10)
        poll = command.get('poll', 0.1)
        expression = command['expression']
        sub_commands = command.get('sub_commands', [])

        end_time = time() + timeout
        while True:
            for sub_cmd in sub_commands:
                self.engine.execute_command(sub_cmd)
            if not self.engine.execute_command({
                    'provider': 'python',
                    'type': 'exec',
                    'expression': expression,
                    }):
                return
            if timeout:
                if time() > end_time:
                    break
            if poll:
                sleep(poll)
        raise TimeoutException(command, timeout)

    def _exec(self, expression, context):
        """ Evaluate a python expression against a given context
        """

        context = context.copy()
        return RestrictionCapableEval(expression).eval(context)
