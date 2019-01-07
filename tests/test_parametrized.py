def test_autoexecute_yml_parametrized_data(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: variables['username'] in ('foò', 'bàr',)
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "bar"}
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)


def test_autoexecute_yml_parametrized_data_passed_failed(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "barZ"}
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=1, failed=1)


def test_autoexecute_yml_parametrized_data_passed_keyword(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "barZ"}
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest('-k yml0')

    result.assert_outcomes(passed=1, failed=0)


def test_autoexecute_yml_parametrized_data_a(testdir):
    yml_file = testdir.makefile(".yml", """
---
- provider: python
  type: assert
  expression: variables['username'] in ('foò', 'bàr',)
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foò"}
            {"username": "bàr"}
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
