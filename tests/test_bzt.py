import pytest


@pytest.mark.parametrize(
    "file_path",
    ["/some/test_path.json", "000aaa.json", "ààà.json", "000"])
def test_bzt_compat(file_path):
    import mock
    from pytest_play.plugin import JSONItem
    item = JSONItem("name", mock.Mock(nodeid="nodeid"), file_path)
    assert item.module.__name__
