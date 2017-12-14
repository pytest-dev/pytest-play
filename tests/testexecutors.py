from pytest_play.executors import JSONExecutorSplinter


def test_splinter_executor_constructor(bdd_vars, parametrizer_class):
    executor = JSONExecutorSplinter(None, bdd_vars, parametrizer_class)
    assert executor.parametrizer_class is parametrizer_class
    assert executor.page is None
    assert executor.variables == bdd_vars


def test_splinter_executor_parametrizer(parametrizer_class):
    executor = JSONExecutorSplinter(None, {'foo': 'bar'}, parametrizer_class)
    assert executor.parametrizer.parametrize('$foo') == 'bar'
