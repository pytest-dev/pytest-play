def test_autoexecute_yml_pass(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: 1
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)


def test_autoexecute_yml_fail(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: 0
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(failed=1)


def test_autoexecute_yml_cli_pass(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: 1
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest(yml_file.strpath)

    result.assert_outcomes(passed=1)
