def test_repeater(testdir):
    testdir.makeconftest("""
import pytest


@pytest.fixture(autouse=True)
def __pytest_repeater_play_test(request):
    pass


@pytest.hookimpl(trylast=True)
def pytest_generate_tests(metafunc):
    metafunc.parametrize(
        '__pytest_repeater_play_test',
        range(2),
        indirect=True,
    )
    """)

    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: "1"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
