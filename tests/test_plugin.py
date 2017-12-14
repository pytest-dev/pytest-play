# -*- coding: utf-8 -*-
from pytest_play.executors import JSONExecutorSplinter


def test_page_timeout(page_timeout):
    assert page_timeout == 20


def test_executor_splinter_class(json_executor_splinter_class):
    assert json_executor_splinter_class is JSONExecutorSplinter
