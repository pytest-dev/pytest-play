import json
import re
from time import (
    sleep,
    time,
)
from RestrictedPython import RestrictionCapableEval
from pytest_play.providers import BaseProvider
import datetime


class TimeoutException(Exception):
    """ Timeout exception """


class PythonProvider(BaseProvider):
    """ Python command provider """

    def _get_context(self, extra_context):
        context = {
            'variables': self.engine.variables,
            'len': len,
            'list': list,
            'match': re.match,
            'datetime': datetime,
            'loads': json.loads,
            'dumps': json.dumps,
            'filter': filter,
            'map': map,
            }
        context.update(extra_context)
        return context

    def command_assert(self, command, **kwargs):
        """ Make an assertion based on a command containing
            a python expression
        """
        expression = command.get('expression', None)
        if expression:
            context = self._get_context(kwargs)
            assert self._exec(
                expression,
                context,
            )

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
        wait_time = int(command['seconds'])
        sleep(wait_time)

    def command_wait_until(self, command, **kwargs):
        """ Wait until an expression is not False
        """
        timeout = command.get('timeout', 10)
        poll = command.get('poll', 0.1)
        expression = command['expression']

        end_time = time() + timeout
        while True:
            for sub_cmd in command['sub_commands']:
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

        end_time = time() + timeout
        while True:
            for sub_cmd in command['sub_commands']:
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
