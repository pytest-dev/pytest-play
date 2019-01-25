def test_autoexecute_yml_parametrized_data(testdir):
    yml_file = testdir.makefile(".yml", """
---
test_data:
  - username: foo
    age: 21
  - username: bar
    age: 22
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)


def test_autoexecute_yml_parametrized_data_uppercase(testdir):
    yml_file = testdir.makefile(".yml", """
---
test_data:
  - Username: Foo
  - Username: Bar
---
- provider: python
  type: assert
  expression: variables['Username'] in ('Foo', 'Bar',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)


def test_autoexecute_yml_parametrized_data_json(testdir):
    """ json syntax """
    yml_file = testdir.makefile(".yml", """
---
test_data:
  [{"username": "foo"},
  {"username": "bar"}]
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)


def test_autoexecute_yml_parametrized_data_passed_failed(testdir):
    yml_file = testdir.makefile(".yml", """
---
test_data:
  - username: foo
  - username: barZ
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=1, failed=1)


def test_autoexecute_yml_parametrized_data_passed_keyword(testdir):
    yml_file = testdir.makefile(".yml", """
---
test_data:
  - username: foo
  - username: barZ
---
- provider: python
  type: assert
  expression: variables['username'] in ('foo', 'bar',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest('-k yml0')

    result.assert_outcomes(passed=1, failed=0)


def test_autoexecute_yml_parametrized_data_a(testdir):
    yml_file = testdir.makefile(".yml", """
---
test_data:
  - username: foò
  - username: bàr
---
- provider: python
  type: assert
  expression: variables['username'] in ('foò', 'bàr',)
    """)
    assert yml_file.basename.startswith('test_')
    assert yml_file.basename.endswith('.yml')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
