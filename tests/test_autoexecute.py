def test_autoexecute_json_pass(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "1"
                }
            ]
        }
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')

    result = testdir.runpytest()

    result.assert_outcomes(passed=1)


def test_autoexecute_json_fail(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "0"
                }
            ]
        }
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')

    result = testdir.runpytest()

    result.assert_outcomes(failed=1)


def test_autoexecute_json_cli_pass(testdir):
    json_file = testdir.makefile(".json", """
        {
            "steps": [
                {
                    "provider": "python",
                    "type": "assert",
                    "expression": "1"
                }
            ]
        }
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')

    result = testdir.runpytest(json_file.strpath)

    result.assert_outcomes(passed=1)
