# -*- coding: utf-8 -*-
import os
import pytest
from .executors import JSONExecutorSplinter


@pytest.fixture
def json_executor_splinter_class():
    """ Splinter based json executor class """
    return JSONExecutorSplinter


@pytest.fixture
def data_getter():
    """ Fixture that returns a callable that returns the files contents
        for a given name
    """
    def _json_executor_data(*tokens):
        data = ''
        with open(
                os.path.join(*tokens),
                'r') as file_obj:
            data = file_obj.read()
        return data
    return _json_executor_data


@pytest.fixture
def default_json_executor_class(json_executor_splinter_class):
    """ The default json executor class. You can easily override it """
    return json_executor_splinter_class


@pytest.fixture
def play_json(default_json_executor_class, bdd_vars,
              parametrizer_class, navigation, variables, skin):
    """
        How to use json_executor::

            def test_experimental(play_json):
                data = data_getter('/my/path/etc', 'login.json')
                play_json.execute(data)
    """
    context = bdd_vars.copy()
    skin_settings = variables['skins'][skin]
    context['base_url'] = skin_settings['base_url']
    for credential_name, credential_settings in \
            skin_settings['credentials'].items():
        username_key = "{0}_name".format(credential_name)
        password_key = "{0}_pwd".format(credential_name)
        context[username_key] = credential_settings['username']
        context[password_key] = credential_settings['password']
    return default_json_executor_class(
        navigation, context, parametrizer_class)
