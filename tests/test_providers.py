import pytest


@pytest.fixture
def dummy_provider(dummy_executor):
    from pytest_play.providers import SplinterCommandProvider
    return SplinterCommandProvider(dummy_executor)


def test_splinter_executor_locator(dummy_provider):
    assert dummy_provider.locator_translate(
        {'type': 'css',
         'value': 'body'}) == ('css', 'body')


def test_splinter_executor_locator_bad(dummy_provider):
    with pytest.raises(ValueError):
        dummy_provider.locator_translate(
            {'type': 'cssXX',
             'value': 'body'}) == ('css', 'body')
