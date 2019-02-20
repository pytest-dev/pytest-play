import pytest
import mock


def test_play_engine_constructor(request):
    from pytest_play.engine import PlayEngine
    executor = PlayEngine(request, {'foo': 'bar'})
    assert executor.request is request
    assert executor.variables == {'foo': 'bar'}


def test_get_file_contents(play, data_base_path):
    play.get_file_contents(data_base_path, 'included.yml')


def test_register_teardown(play, data_base_path):
    assert play._teardown == []
    import mock
    callback = mock.MagicMock()
    play.register_teardown_callback(callback)
    play.register_teardown_callback(callback)
    assert callback in play._teardown
    assert len(play._teardown) == 1
    assert not callback.called
    play.teardown()
    assert callback.assert_called_once_with() is None


def test_executor_parametrizer(dummy_executor):
    assert dummy_executor.parametrizer.parametrize('$foo') == 'bar'


def test_execute(dummy_executor):
    execute_command_mock = mock.MagicMock()
    dummy_executor.execute_command = execute_command_mock

    yml_data = [
        {'provider': 'python', 'type': 'assert', 'expression': '1'},
        {'provider': 'python', 'type': 'assert', 'expression': '2'}
    ]
    dummy_executor.execute(yml_data)

    calls = [
        mock.call(yml_data[0]),
        mock.call(yml_data[1]),
    ]
    assert dummy_executor.execute_command.assert_has_calls(
        calls, any_order=False) is None


def test_execute_extra_vars(dummy_executor):
    execute_command_mock = mock.MagicMock()
    dummy_executor.execute_command = execute_command_mock

    yml_data = [
        {'provider': 'python', 'type': 'assert', 'expression': '1'},
        {'provider': 'python', 'type': 'assert',
         'expression': '2 == $does_not_exist'}
    ]
    assert 'does_not_exist' not in dummy_executor.variables
    dummy_executor.execute(yml_data, extra_variables={'does_not_exist': '2'})

    calls = [
        mock.call(yml_data[0]),
        mock.call(yml_data[1]),
    ]
    assert dummy_executor.execute_command.assert_has_calls(
        calls, any_order=False) is None


def test_execute_bad_type(dummy_executor):
    command = {'provider': 'python', 'typeXX': 'assert', 'expression': '1'}
    with pytest.raises(KeyError):
        dummy_executor.execute_command(command)


def test_execute_bad_command(dummy_executor):
    command = {'provider': 'python', 'type': 'assert', 'expressionXX': '1'}
    with pytest.raises(KeyError):
        dummy_executor.execute_command(command)


def test_execute_not_implemented_command(dummy_executor):
    command = {'provider': 'python', 'type': 'new_command',
               'param': 'http://1'}
    dummy_executor.COMMANDS = ['new_command']
    with pytest.raises(NotImplementedError):
        dummy_executor.execute_command(command)


def test_execute_condition_true(dummy_executor):
    command = {'provider': 'python',
               'type': 'assert',
               'expression': 'False',
               'skip_condition': '1 == 1'}
    dummy_executor.execute_command(command)


def test_execute_condition_false(dummy_executor):
    command = {'provider': 'python',
               'type': 'assert',
               'expression': 'True',
               'skip_condition': '1 == 0'}
    dummy_executor.execute_command(command)


def test_execute_get_basestring(dummy_executor):
    import yaml
    command = yaml.load("""
---
provider: python
type: assert
expression: 1 == 1
    """)
    dummy_executor.execute_command(command)


def test_execute_get_basestring_param(dummy_executor):
    import yaml
    command = yaml.load("""
---
provider: python
type: assert
expression: "'$foo' == 'bar'"
""")
    dummy_executor.execute_command(command)


def test_new_provider_custom_command(dummy_executor):
    command = {'type': 'newCommand', 'provider': 'newprovider'}
    dummy_provider = mock.MagicMock()

    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)
    dummy_executor.register_command_provider(
        dummy_provider, 'newprovider')

    # execute new custom command
    dummy_executor.execute_command(command)

    assert dummy_provider.assert_called_once_with(dummy_executor) is None
    assert dummy_provider \
        .return_value \
        .command_newCommand \
        .assert_called_once_with(command) is None


def test_execute_includes(dummy_executor, data_base_path):

    yml_data = [
        {'type': 'include', 'provider': 'include',
         'path': '{0}/{1}'.format(
             data_base_path, 'included.yml')},
        {'type': 'include', 'provider': 'include',
         'path': '{0}/{1}'.format(
             data_base_path, 'assertion.yml')},
    ]
    dummy_executor.execute(yml_data)

    assert dummy_executor.variables['included'] == 1


def test_default_command(play, data_base_path):
    play.variables['include'] = {'comment': 'default comment'}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = 'default comment'
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_default_command_override(play, data_base_path):
    play.variables['include'] = {'comment': 'default comment'}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "comment": "override",
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = 'override'
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_default_command_override_dict(play, data_base_path):
    play.variables['include'] = {
        'comment': {'comment': 'default comment'}}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "comment": {"another": "override"},
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = {
        'another': 'override', 'comment': 'default comment'}
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_default_command_override_dict_2(play, data_base_path):
    play.variables['include'] = {
        'comment': {'comment': 'default comment'}}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "comment": {"another": "override", "comment": "other"},
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = {
        'another': 'override', 'comment': 'other'}
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_default_command_override_dict_4(
        play, data_base_path):
    play.variables['include'] = {
        'comment': {'comment': 'default comment'}}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "comment": "default comment",
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = 'default comment'
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_default_command_override_dict_3(
        play, data_base_path):
    play.variables['include'] = {
        'comment': 'default comment'}
    play.get_command_provider = mock.MagicMock()
    yml_data = [
        {"provider": "include", "type": "include",
         "comment": {"another": "override", "comment": "other"},
         "path": "{0}/included.yml".format(data_base_path)},
    ]
    from copy import deepcopy
    expected_command = deepcopy(yml_data)[0]
    expected_command['comment'] = {
        'another': 'override', 'comment': 'other'}
    play.execute(yml_data)
    assert play \
        .get_command_provider \
        .return_value \
        .command_include \
        .assert_called_once_with(
            expected_command) is None


def test_include_string(play, data_base_path):
    play.variables['foo'] = 'bar'
    yml_data = """
---
- provider: include
  type: include
  path: "%s/included.yml"
- provider: python
  type: assert
  expression: "$included == 1"
- provider: python
  type: store_variable
  name: included
  expression: "2"
  comment: update included value from 1 to 2
- provider: python
  type: assert
  expression: "$included == 2"
    """ % data_base_path
    play.execute_raw(yml_data)
    assert play.variables['included'] == 2


def test_teardown(play):
    import mock
    play._teardown = [
        mock.MagicMock(side_effect=AttributeError()),
        mock.MagicMock()]
    play.teardown()
    assert play._teardown[0].assert_called_once_with() is None
    assert play._teardown[1].assert_called_once_with() is None


def test_record_property(play):
    import mock
    play.request = mock.MagicMock()
    play.record_property('name', '1')
    assert play.request.getfixturevalue.assert_called_once_with(
        'record_property') is None
    assert play.request.getfixturevalue.return_value.assert_called_once_with(
        'name', '1') is None


def test_elapsed_variable(play):
    command = {'provider': 'python',
               'type': 'assert',
               'expression': 'True', }
    assert 'elapsed' not in play.variables
    play.execute_command(command)
    assert float(play.variables['elapsed']) > 0
