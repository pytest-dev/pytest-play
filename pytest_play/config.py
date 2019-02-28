try:
    __import__('statsd')
except ImportError:
    STATSD = False
else:
    STATSD = True

try:
    __import__('pytest_statsd')
except ImportError:
    PYTEST_STATSD = False
else:
    PYTEST_STATSD = True
