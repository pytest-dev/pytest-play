from . import BaseProvider


class MetricsProvider(BaseProvider):
    """ PlayEngine wrapper """

    def command_record_property(self, command, **kwargs):
        """ Metrics scenario """
        name = command['name']
        expression = command['expression']
        value = self.engine.execute_command(
            {'provider': 'python',
             'type': 'exec',
             'expression': expression})
        self.engine.update_variables({name: value})
        self.engine.record_property(name, value)

    def command_record_elapsed(self, command, **kwargs):
        """ Metrics scenario """
        name = command['name']
        value = self.engine.variables['_elapsed']
        self.engine.update_variables({name: value})
        self.engine.record_property(name, value)
