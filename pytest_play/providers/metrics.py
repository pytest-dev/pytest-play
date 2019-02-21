from . import BaseProvider


class MetricsProvider(BaseProvider):
    """ PlayEngine wrapper """

    def command_record_property(self, command, **kwargs):
        """ Metrics scenario """
        name = command['name']
        value = self.engine.variables['_elapsed']
        self.engine.update_variables({name: value})
        self.engine.record_property(name, value)
