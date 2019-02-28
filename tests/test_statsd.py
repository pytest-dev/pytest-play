

def run(testdir, stats_d=True, stats_prefix=None, stats_host=None,
        stats_port=None):
    args = []
    if stats_d is not None:
        args.append('--stats-d')
        if stats_prefix is not None:
            args.append('--stats-prefix')
            args.append(stats_prefix)
        if stats_host is not None:
            args.append('--stats-host')
            args.append(stats_host)
        if stats_port is not None:
            args.append('--stats-port')
            args.append(stats_port)
    args.append('-s')
    return testdir.runpytest(*args)


def test_statsd_cli(testdir):
    testdir.makepyfile("""
def test_statsd_cli(request):
    assert request.config.getoption('stats_d')
    assert request.config.getoption('stats_host') == 'http://'
    assert request.config.getoption('stats_port') == '80'
    assert request.config.getoption('stats_prefix') == 'prefix'
    assert 1
    """)
    result = run(
        testdir, stats_d=True,
        stats_host='http://', stats_port='80',
        stats_prefix='prefix')
    assert result.ret == 0
