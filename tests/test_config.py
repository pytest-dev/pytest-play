# -*- coding: utf-8 -*-
def test_statsd():
    from pytest_play.config import STATSD
    assert STATSD is True


def test_pytest_statsd():
    from pytest_play.config import PYTEST_STATSD
    assert PYTEST_STATSD is False
