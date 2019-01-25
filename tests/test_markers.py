import pytest


@pytest.mark.parametrize("cli_options", [
    ('-m', 'not marker1',),
])
def test_autoexecute_yml_markers_skipped(testdir, cli_options):
    yml_file = testdir.makefile(".yml", """
---
markers:
  - marker1
  - marker2
---
- provider: python
  type: assert
  expression: "1"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest(*cli_options)

    result.assert_outcomes(passed=0, failed=0, error=0)
    # Deselected, not skipped. See #3427
    # result.assert_outcomes(skipped=1)


def test_autoexecute_yml_markers_passed(testdir):
    yml_file = testdir.makefile(".yml", """
---
markers:
  - marker1
  - marker2
---
- provider: python
  type: assert
  expression: "1"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest('-m marker1')

    result.assert_outcomes(passed=1)


def test_autoexecute_yml_markers_strict_passed(testdir):
    yml_file = testdir.makefile(".yml", """
---
markers:
  - marker1
  - marker2
---
- provider: python
  type: assert
  expression: "1"
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest('-m marker1 --strict')

    result.assert_outcomes(passed=1)
