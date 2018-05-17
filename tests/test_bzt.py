import pytest
from py.path import local


@pytest.mark.parametrize(
    "file_path",
    ["/some/test_path.json",
     "000aaa.json",
     "ààà.json",
     "000",
     local("some/test_path.json")])
def test_bzt_compat(file_path):
    import mock
    from pytest_play.plugin import JSONItem
    item = JSONItem("name", mock.Mock(nodeid="nodeid"), file_path)
    assert isinstance(item.path, str)
    assert item.path == getattr(file_path, 'strpath', file_path)
    assert item.module.__name__
