# -*- coding: utf-8 -*-
import os
from pypom import Page
import pytest
from .executors import JSONExecutorSplinter


@pytest.fixture
def json_executor_splinter_class():
    """ Splinter based json executor class """
    return JSONExecutorSplinter


@pytest.fixture
def json_executor_data_getter(json_data_base_path, parametrizer):
    """ Fixture that returns a callable that returns the files contents
        for a given name
    """
    def _json_executor_data(*tokens):
        data = ''
        with open(
                os.path.join(*tokens),
                'r') as file_obj:
            data = file_obj.read()
        return parametrizer.json_loads(data)
    return _json_executor_data


@pytest.fixture
def default_json_executor_class(json_executor_splinter_class):
    """ The default json executor class. You can easily override it """
    return json_executor_splinter_class


@pytest.fixture
def pypom_page_class():
    """ PyPOM page class """
    return Page


@pytest.fixture
def page_timeout():
    """ Default page timeout """
    return 20


@pytest.fixture
def page(pypom_page_class, browser, page_timeout):
    """ Basic page implementation based on pypom_page_class"""
    return Page(browser, timeout=page_timeout)


@pytest.fixture
def json_executor(default_json_executor_class, page, bdd_vars,
                  parametrizer_class):
    """
        How to use json_executor:

        def test_experimental(json_executor, json_executor_data_getter):
            data = json_executor_data_getter('login.json')
            json_executor.execute(data)
    """
    return default_json_executor_class(page, bdd_vars, parametrizer_class)
