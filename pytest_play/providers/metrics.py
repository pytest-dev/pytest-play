import time

from . import BaseProvider


class MetricsProvider(BaseProvider):
    """ PlayEngine wrapper """

    def command_record_property(self, command, **kwargs):
        """ record a property (dynamic expression) """
        name = command['name']
        expression = command['expression']
        value = self.engine.execute_command(
            {'provider': 'python',
             'type': 'exec',
             'expression': expression})
        self.engine.update_variables({name: value})
        self.engine.record_property(name, value)

    def command_record_elapsed(self, command, **kwargs):
        """ record a property (previous command elapsed) """
        name = command['name']
        value = self.engine.variables['_elapsed']
        self.engine.update_variables({name: value})
        self.engine.record_property(name, value)

    def command_record_elapsed_start(self, command, **kwargs):
        """ record a time delta (start tracking time) """
        name = command['name']
        self.engine.update_variables({name: time.time()})

    def command_record_elapsed_end(self, command, **kwargs):
        """ record a time delta (end tracking time) """
        name = command['name']
        delta = time.time() - self.engine.variables[name]
        self.engine.update_variables({name: delta})
        self.engine.record_property(name, delta)
