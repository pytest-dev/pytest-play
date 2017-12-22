# -*- coding: utf-8 -*-
import json
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
        if not isinstance(data, basestring):
            # if not dic reparametrize
            data = self.parametrizer.parametrize(json.dumps(data))
        return self.parametrizer.json_loads(data)

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

    def register_steps(self, data, name):
        """
            You can register a group of actions as a pytest play provider and
            **include** them in other scenario for improved reusability.

            For example let's pretend we want to reuse the login steps coming
            from a ``login.json`` file::

                import pytest


                @pytest.fixture(autouse=True)
                def login_procedure(play_json, data_getter):
                    data = data_getter('/my/path/etc', 'login.json')
                    play_json.register_steps(
                        data, 'login.json')

                def test_like(play_json, data_getter):
                    data = data_getter('/my/path/etc', 'like.json')
                    play_json.execute(data)


            where ``like.json`` contains the steps coming from the included
            ``login.json`` file plus additional actions::

                {
                    "steps": [
                            {
                                    "provider": "login.json"
                                    "type": "include"
                            },
                            {
                                    "type": "clickElement",
                                    "locator": {
                                            "type": "css",
                                            "value": ".like"
                                    }
                            }
                    ]
                }

            **NOTE WELL**: it's up to you avoid recursion issues.
        """
        class IncludeProvider(object):
            """ PlayEngine wrapper """

            def __init__(self, engine):
                self.engine = engine

            def command_include(self, command):
                self.engine.execute(
                    self.engine.parametrizer.parametrize(data)
                )

        self.register_command_provider(IncludeProvider, name)
