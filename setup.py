#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import (
    setup,
    find_packages,
)


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


install_requires = [
    'pytest>=3.0.7',
    'pytest-variables[yaml]',
    'zope.interface',
    'zope.component',
    'RestrictedPython>=4.0b2',
    'parametrizer>=0.0.3',
]

statsd_require = [
    'statsd',
]

tests_require = [
    'pytest-cov',
    'mock',
    'py',
]

docs_require = [
    'Sphinx',
    'sphinx_rtd_theme',
    ]

setup(
    name='pytest-play',
    version='2.3.0',
    author='Davide Moro',
    author_email='davide.moro@gmail.com',
    maintainer='Davide Moro',
    maintainer_email='davide.moro@gmail.com',
    license='Apache Software License 2.0',
    url='https://github.com/davidemoro/pytest-play',
    description='pytest plugin that let you automate actions '
                'and assertions with test metrics reporting '
                'executing plain YAML files',
    long_description=open("README.rst").read() + "\n" +
    open("CHANGES.rst").read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'playcommands': [
            'include = pytest_play.providers:IncludeProvider',
            'python = pytest_play.providers:PythonProvider',
            'metrics = pytest_play.providers:MetricsProvider',
        ],
        'pytest11': [
            'pytest-play = pytest_play.plugin',
        ],
    },
    extras_require={
        'statsd': statsd_require,
        'tests': tests_require,
        'docs': docs_require,
    },
)
