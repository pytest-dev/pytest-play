import pytest
import mock


@pytest.fixture
def dummy_default_provider(dummy_executor):
    from pytest_play.providers import SplinterCommandProvider
    return SplinterCommandProvider(dummy_executor)


@pytest.fixture
def dummy_include_provider():
    from pytest_play.providers import register_steps
    return register_steps


def test_splinter_executor_locator(dummy_default_provider):
    assert dummy_default_provider.locator_translate(
        {'type': 'css',
         'value': 'body'}) == ('css', 'body')


def test_splinter_executor_locator_bad(dummy_default_provider):
    with pytest.raises(ValueError):
        dummy_default_provider.locator_translate(
            {'type': 'cssXX',
             'value': 'body'}) == ('css', 'body')


def test_include_provider(dummy_include_provider):
    mock_executor = mock.MagicMock()
    data = '{"steps":[]}'
    provider = dummy_include_provider(data)(mock_executor)
    provider.command_include({})
    assert provider.engine.execute.assert_called_once_with(data) is None


def test_include_provider_variation(dummy_include_provider):
    mock_executor = mock.MagicMock()
    data = {"steps": []}
    provider = dummy_include_provider(data)(mock_executor)
    provider.command_include({})
    assert provider.engine.execute.assert_called_once_with(data) is None
