def test_autoexecute_json_parametrized_data(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "variables['username'] in ('foo', 'bar',)"
                }
            ]
        }
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "bar"}
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)


def test_autoexecute_json_parametrized_data_passed_failed(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "variables['username'] in ('foo', 'bar',)"
                }
            ]
        }
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "barZ"}
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=1, failed=1)


def test_autoexecute_json_parametrized_data_passed_keyword(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "variables['username'] in ('foo', 'bar',)"
                }
            ]
        }
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foo"}
            {"username": "barZ"}
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest('-k json0')

    result.assert_outcomes(passed=1, failed=0)


def test_autoexecute_json_parametrized_data_a(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "variables['username'] in ('foò', 'bàr',)"
                }
            ]
        }
    """)
    ini_file = testdir.makefile(".ini", """
        [pytest]
        test_data =
            {"username": "foò"}
            {"username": "bàr"}
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest()

    result.assert_outcomes(passed=2)
