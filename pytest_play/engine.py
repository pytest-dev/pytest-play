# -*- coding: utf-8 -*-
import os
import json
import re
import datetime
import logging
import yaml
import pkg_resources
import time
from zope import component
from zope.interface import Interface
from parametrizer import Parametrizer


logger = logging.getLogger(__name__)


class ICommandProvider(Interface):
    """ Marker for pytest play command provider """


class PlayEngine(object):
    """ YAML executor """

    _context = {
        'len': len,
        'list': list,
        'match': re.match,
        'datetime': datetime,
        'loads': json.loads,
        'dumps': json.dumps,
        'filter': filter,
        'map': map,
        'sorted': sorted,
        'int': int,
        'float': float,
        }

    def __init__(self, request, variables):
        """ The executor should be initialized with:
            * **request**. A pytest ``request`` fixture that will be used
              for looking up other fixtures
            * **variables**. A dictionary that wil be used for parametrize
              commands
        """
        self.request = request
        self.variables = variables
        self.gsm = component.getGlobalSiteManager()

        self.register_plugins()
        self._teardown = []

    def register_teardown_callback(self, callback):
        """ Register teardown callback """
        if callback not in self._teardown:
            self._teardown.append(callback)

    def teardown(self):
        """ Teardown """
        for callback in self._teardown:
            try:
                callback()
            except Exception:
                pass

    def get_file_contents(self, *tokens):
        """ Return file contents """
        data = ''
        with open(
                os.path.join(*tokens),
                'r') as file_obj:
            data = file_obj.read()
        return data

    @property
    def context(self):
        context = self._context
        context['variables'] = self.variables
        return context

    def parametrize(self, data):
        """ Parametrize data """
        return Parametrizer(
            self.context['variables'],
            context=self.context).parametrize(data)

    def _yaml_loads(self, data):
        """ returns parametrized yaml dumps """
        return yaml.safe_load(
            self.parametrize(data))

    def _merge_payload(self, command):
        """ Merge command with the default command available in
            engine.variables['provider']
        """
        provider = command['provider']
        provider_conf = self.variables.get(provider, {})
        if provider_conf:
            default = self._yaml_loads(
                yaml.dump(provider_conf, default_flow_style=False))
            if provider_conf:
                return self._merge(default, command)
        return command

    def _merge(self, a, b, path=None):
        """ merges b and a configurations.
            Based on http://bit.ly/2uFUHgb
         """
        if path is None:
            path = []

        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self._merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    # b wins
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def skip_condition(func):
        """ Skip command if skip_condition python expression is falsish  """
        def wrapper(*args, **kwargs):
            command = args[0]._yaml_loads(
                yaml.dump(args[1], default_flow_style=False))
            condition = command.get('skip_condition', None)
            skip = False
            if condition is not None:
                expr = args[0].parametrize(condition)
                if args[0].execute_command(
                    {'provider': 'python',
                     'type': 'exec',
                     'expression': expr
                     }):
                    skip = True
            if not skip:
                return func(*args, **kwargs)
        return wrapper

    def execute_raw(self, data, extra_variables={}):
        """ Execute raw yaml-like file contents """
        if extra_variables:
            self.update_variables(extra_variables)
        self.execute(list(yaml.safe_load_all(data))[-1])

    def execute(self, data, extra_variables={}):
        """ Execute parsed yaml-like file contents """
        if extra_variables:
            self.update_variables(extra_variables)
        for step in data:
            self.execute_command(step)

    @skip_condition
    def execute_command(self, command, **kwargs):
        """ Execute single command """
        return_value = None
        command = self._merge_payload(
            self._yaml_loads(
                yaml.dump(
                    command, default_flow_style=False))
        )
        command_type = command['type']
        provider_name = command.get('provider', 'default')
        command_provider = self.get_command_provider(provider_name)

        if command_provider is None:
            logger.error('Not supported provider %r', command)
            raise ValueError('Command not supported',
                             command_type,
                             provider_name)

        method_name = 'command_{0}'.format(command_type)

        method = getattr(command_provider, method_name, None)
        if method is None:
            logger.error('Not supported command %r', command)
            raise NotImplementedError(
                'Command not implemented', command_type, provider_name)
        logger.info('Executing command %r', command)

        start_time = time.time()
        try:
            return_value = method(command, **kwargs)
        except Exception:
            logger.error('FAILED command %r', command)
            logger.info('DUMP variables %r', self.variables)
            print(self.variables)
            raise
        finally:
            elapsed = time.time() - start_time
            print(dict(command, _elapsed=elapsed))
            self.update_variables({'_elapsed': elapsed})
        return return_value

    def update_variables(self, extra_variables):
        """ Update variables """
        self.variables.update(extra_variables)
        logger.debug("Variables updated %r", self.variables)

    # register commands
    def register_plugins(self):
        """ Auto register plugins and command providers"""
        for entrypoint in pkg_resources.iter_entry_points('playcommands'):
            plugin = entrypoint.load()
            self.register_command_provider(plugin, entrypoint.name)

    def register_command_provider(self, factory, name):
        """ Register command provider """
        self.gsm.registerUtility(
            factory(self),
            ICommandProvider,
            name,
        )

    def get_command_provider(self, name):
        """ Get command provider by name """
        return component.queryUtility(ICommandProvider, name=name)
