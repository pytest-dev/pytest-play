import pytest


@pytest.mark.parametrize("cli_options", [
    ('-k', 'notestdeselect',),
])
def test_autoexecute_yml_keywords_skipped(testdir, cli_options):
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
