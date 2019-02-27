import time

from ..config import STATSD
from . import BaseProvider


class MetricsProvider(BaseProvider):
    """ PlayEngine wrapper """
    def __init__(self, *args, **kwargs):
        super(MetricsProvider, self).__init__(*args, **kwargs)
        self._record_property = self.engine.request.getfixturevalue(
            'record_property')

    @property
    def statsd_client(self):
        import statsd
        host = self.engine.request.config.getoption('stats_host')
        port = self.engine.request.config.getoption('stats_port')
        prefix = self.engine.request.config.getoption('stats_prefix')
        return statsd.StatsClient(host, port, prefix=prefix)

    def record_property(self, name, value, metric_type='timing'):
        """ Record a property metrics """
        self._record_property(name, value)
        if STATSD:
            statsd_client = self.statsd_client
            method = None
            if metric_type == 'timing':
                method = statsd_client.timing
            elif metric_type == 'gauge':
                method = statsd_client.gauge
            if method is not None:
                method(name, value)

    def command_record_property(self, command, **kwargs):
        """ record a property (dynamic expression) """
        name = command['name']
        expression = command['expression']
        value = self.engine.execute_command(
            {'provider': 'python',
             'type': 'exec',
             'expression': expression})
        self.engine.update_variables({name: value})
        self.record_property(name, value)

    def command_record_elapsed(self, command, **kwargs):
        """ record a property (previous command elapsed) """
        name = command['name']
        value = self.engine.variables['_elapsed']
        self.engine.update_variables({name: value})
        self.record_property(name, value)

    def command_record_elapsed_start(self, command, **kwargs):
        """ record a time delta (start tracking time) """
        name = command['name']
        self.engine.update_variables({name: time.time()})

    def command_record_elapsed_stop(self, command, **kwargs):
        """ record a time delta (end tracking time) """
        name = command['name']
        delta = time.time() - self.engine.variables[name]
        self.engine.update_variables({name: delta})
        self.record_property(name, delta)
