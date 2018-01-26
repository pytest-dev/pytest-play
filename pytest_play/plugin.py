# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def play_engine_class():
    """ Play engine class  class """
    from .engine import PlayEngine
    return PlayEngine


@pytest.fixture
def play_json(request, play_engine_class, bdd_vars, variables, skin):
    """
        How to use json_executor::

            def test_experimental(play_json):
                data = play_json.get_file_contents(
                    '/my/path/etc', 'login.json')
                play_json.execute(data)
    """
    context = bdd_vars.copy()
    if 'skins' in variables:
        skin_settings = variables['skins'][skin]
        if 'base_url' in skin_settings:
            context['base_url'] = skin_settings['base_url']
        if 'credentials' in skin_settings:
            for credential_name, credential_settings in \
                    skin_settings['credentials'].items():
                username_key = "{0}_name".format(credential_name)
                password_key = "{0}_pwd".format(credential_name)
                context[username_key] = credential_settings['username']
                context[password_key] = credential_settings['password']
    play_json = play_engine_class(request, context)
    yield play_json
    play_json.teardown()
