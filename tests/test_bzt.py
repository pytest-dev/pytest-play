import pytest
from py.path import local


@pytest.mark.parametrize(
    "file_path",
    [local("/some/test_path.yml"),
     local("000aaa.yml"),
     local("ààà.yml"),
     local("000"),
     local("some/test_path.yml")])
def test_bzt_compat(file_path):
    import mock
    from pytest_play.plugin import YAMLItem
    item = YAMLItem(
        "name", parent=mock.Mock(nodeid="nodeid", fspath=file_path))
    assert isinstance(item.path, str)
    assert item.path == getattr(file_path, 'strpath', file_path)
    assert item.module.__name__
