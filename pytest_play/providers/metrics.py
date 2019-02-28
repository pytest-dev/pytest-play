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

    def _record_property_statsd(
            self, name, value, metric_type=None, meas_unit=None):
        if STATSD:
            if metric_type is not None:
                statsd_client = self.statsd_client
                method = None
                if metric_type == 'timing':
                    method = statsd_client.timing
                    if meas_unit == 's':
                        value = value * 1000
                    assert float(value)
                elif metric_type == 'gauge':
                    method = statsd_client.gauge
                    assert float(value)
                else:
                    raise ValueError("metric_type not valid: ", metric_type)
                if method is not None:
                    method(name, value)

    def record_property(self, name, value, metric_type=None, meas_unit=None):
        """ Record a property metrics """
        self._record_property_statsd(
            name, value, metric_type=metric_type, meas_unit=meas_unit)
        self._record_property(name, value)

    def command_record_property(self, command, **kwargs):
        """ record a property (dynamic expression) """
        name = command['name']
        expression = command['expression']
        metric_type = command.get('metric_type', None)
        value = self.engine.execute_command(
            {'provider': 'python',
             'type': 'exec',
             'expression': expression})
        self.record_property(name, value, metric_type=metric_type)
        self.engine.update_variables({name: value})

    def command_record_elapsed(self, command, **kwargs):
        """ record a property (previous command elapsed) """
        name = command['name']
        value = self.engine.variables['_elapsed']
        self.engine.update_variables({name: value})
        self.record_property(name, value, metric_type='timing',
                             meas_unit='s')

    def command_record_elapsed_start(self, command, **kwargs):
        """ record a time delta (start tracking time) """
        name = command['name']
        self.engine.update_variables({name: time.time()})

    def command_record_elapsed_stop(self, command, **kwargs):
        """ record a time delta (end tracking time) """
        name = command['name']
        delta = time.time() - self.engine.variables[name]
        self.engine.update_variables({name: delta})
        self.record_property(name, delta, metric_type='timing',
                             meas_unit='s')
