import pytest


@pytest.fixture
def conftest_contents():
    return """
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
"""


def test_repeater(testdir, conftest_contents):
    testdir.makeconftest(conftest_contents)

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


def test_repeater_test_data(testdir, conftest_contents):
    testdir.makeconftest(conftest_contents)

    yml_file = testdir.makefile(".yml", """
test_data:
  - mydata: 1
  - mydata: 2
---
- provider: python
  type: assert
  expression: "variables['mydata'] < 3"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=4)


def test_repeater_test_data_failing(testdir, conftest_contents):
    testdir.makeconftest(conftest_contents)

    yml_file = testdir.makefile(".yml", """
test_data:
  - mydata: 1
  - mydata: 2
  - mydata: 3
---
- provider: python
  type: assert
  expression: "variables['mydata'] < 3"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=4, failed=2)
