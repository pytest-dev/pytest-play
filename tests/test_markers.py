import pytest


@pytest.mark.skip(reason="pytest bug?")
def test_autoexecute_json_markers_skipped(testdir):
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
    ini_file = testdir.makefile(".ini", """
        [pytest]
        markers =
            marker1
            marker2
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest('-m "not marker1"')

    result.assert_outcomes(skipped=1)


def test_autoexecute_json_markers_passed(testdir):
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
    ini_file = testdir.makefile(".ini", """
        [pytest]
        markers =
            marker1
            marker2
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest('-m marker1')

    result.assert_outcomes(passed=1)


def test_autoexecute_json_markers_strict_passed(testdir):
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
    ini_file = testdir.makefile(".ini", """
        [pytest]
        markers =
            marker1
            marker2
    """)
    assert json_file.basename.startswith('test_')
    assert json_file.basename.endswith('.json')
    assert ini_file.basename.startswith('test_')
    assert ini_file.basename.endswith('.ini')

    result = testdir.runpytest('-m marker1 --strict')

    result.assert_outcomes(passed=1)
