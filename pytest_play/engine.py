# -*- coding: utf-8 -*-
try:
    # python3
    from builtins import str as basestring
except ImportError:
    # python2
    pass
from zope import component
from zope.interface import Interface
from pypom_navigation.parametrizer import Parametrizer
from .providers import SplinterCommandProvider


class ICommandProvider(Interface):
    """ Marker for pytest play command provider """


class PlayEngine(object):
    """ JSON executor """

    def __init__(self, navigation, variables, parametrizer_class=None):
        self.navigation = navigation
        self.variables = variables
        self.parametrizer_class = parametrizer_class and \
            parametrizer_class or Parametrizer
        self.gsm = component.getGlobalSiteManager()

        self.register_command_provider(SplinterCommandProvider, 'default')

    @property
    def parametrizer(self):
        """ Parametrizer engine """
        return self.parametrizer_class(self.variables)

    def _json_loads(self, data):
        """ If data is a string returns json dumps """
        if isinstance(data, basestring):
            data = self.parametrizer.json_loads(data)
        return data

    def execute(self, data):
        """ Execute parsed json-like file contents """
        data = self._json_loads(data)
        steps = data['steps']
        for step in steps:
            self.execute_command(step)

    def execute_command(self, command):
        """ Execute single command """
        command = self._json_loads(command)
        command_type = command['type']
        provider_name = command.get('provider', 'default')
        command_provider = self.get_command_provider(provider_name)

        if command_provider is None:
            raise ValueError('Command not supported',
                             command_type,
                             provider_name)

        method_name = 'command_{0}'.format(command_type)

        method = getattr(command_provider, method_name, None)
        if method is None:
            raise NotImplementedError(
                'Command not implemented', command_type, provider_name)
        method(command)

    # register commands
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
