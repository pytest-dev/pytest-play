def test_autoexecute_json_markers_pass(testdir):
    json_file = testdir.makefile(".json", """
        {
            "markers": ["marker1", "marker2"],
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

    result = testdir.runpytest('-m "marker1"')

    result.assert_outcomes(passed=1)
