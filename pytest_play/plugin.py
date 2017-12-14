# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope='session')
def skin():
    """ This fixture provides the skin associated with the application
        on which starts the test session.


        For example:

            @pytest.fixture(scope='session',
                            params=mypackage.DEFAULT_PAGES.keys())
            def skin(request):
                return request.param
    """
    return 'skin1'
