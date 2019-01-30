Changelog
=========

2.0.1 (2019-01-30)
------------------

Documentation:

- Mention davidemoro/pytest-play docker container in README.
  You can use pytest-play with a docker command like that now
  ``docker run -i --rm -v $(pwd):/src davidemoro/pytest-play``

Bugfix:

- Fix error locking pipenv due to pytest-play requirement
  constraint not existing (RestrictedPython>=4.0.b2 -> RestrictedPython>=4.0b2)


2.0.0 (2019-01-25)
------------------

Breaking changes:

- Renamed fixture from `play_json` to `play` (#5)

- Drop json support, adopt yaml only format for scenarios (#5)

- Drop ``.ini`` file for metadata, if you need them you can add
  a YAML document on top of the scenario ``.yml`` file. You no more
  need multiple files for decorating your scenarios now (#65)

- `play.execute` no more accepts raw data string), consumes a list of commands.
  Introduced `play.execute_raw` accepting raw data string.

- `play.execute_command` accepts a Python dictionary only now (not a string)

- Selenium provider removed from ``pytest-play`` core, implemented on a
  separate package ``play_selenium``. Starting from now you have to add
  to your selenium commands ``provider: selenium``

- engine's ``parametrizer_class`` attribute no more available (
  use ``parametrizer.Parametrizer`` by default now)

Bug fix:

- Fix invalid markup on PyPI (#55)

- Fix invalid escape sequences (#62).

Documentation and trivial changes:

- Add examples folder


1.4.2 (2018-05-17)
------------------

- Configuration change on Github. Use the same branching policy adopted by
  pytest (master becomes main branch, see #56)

- Fixed skipped test and added new tests (deselect scenarios with keyword
  and marker expressions)

- Fix #58: you no more get a TypeError if you try to launch pytest-play
  in autodiscovery mode

- Fix #55: restructured text lint on README.rst (bad visualization on pypi)

- Updated README (articles and talks links)

- Added a ``DeprecationWarning`` for `play_json` fixture.
  pytest-play will be based on yaml instead of json in version >=2.0.0.
  See https://github.com/pytest-dev/pytest-play/issues/5


1.4.1 (2018-04-06)
------------------

- Documentation improvements

- Add bzt/Taurus/BlazeMeter compatibility


1.4.0 (2018-04-05)
------------------

- Small documentation improvements

- Now ``test_XXX.json`` files are automatically collected and executed

- You can run a test scenario using the pytest CLI ``pytest test_YYY.json``

- Introduced json test scenario ini file with markers definition. For a given
  ``test_YYY.json`` scenario you can add a ``test_YYY.ini`` ini file::

    [pytest]
    markers =
        marker1
        marker2

  and filter scenarios using marker expressions ``pytest -m marker1``

- Enabled parametrization of arguments for a plain json scenario in scenario ini file::

    [pytest]
    test_data =
       {"username": "foo"}
       {"username": "bar"}

  and your json scenario will be executed twice

- ``pytest-play`` loads some variables based on the contents of the optional ``pytest-play``
  section in your ``pytest-variables`` file now. So if your variables file contains the following
  values::

    pytest-play:
      foo: bar
      date_format: YYYYMMDD

  you will be able to use expressions ``$foo``, ``$date_format``, ``variables['foo']`` or
  ``variables['date_format']``


1.3.2 (2018-02-05)
------------------

- Add ``sorted`` in python expressions


1.3.1 (2018-01-31)
------------------

- Add more tests

- Documentation update

- play_json fixture no more assumes that you
  have some pytest-variables settings.
  No more mandatory

- fix include scenario bug that occurs only
  on Windows (slash vs backslash and
  JSON decoding issues)


1.3.0 (2018-01-22)
------------------

- documentation improvements

- supports teardown callbacks


1.2.0 (2018-01-22)
------------------

- implement python based commands in ``pytest-play`` and
  deprecates ``play_python``.
  So this feature is a drop-in replacement for the
  ``play-python`` plugin.

  You should no more install ``play_python`` since now.

- update documentation

- deprecate selenium commands (they will be implemented
  on a separate plugin and dropped in
  ``pytest-play`` >= 2.0.0). All your previous scripts
  will work fine, this warning is just for people
  directly importing the provider for some reason.

- implement skip conditions. You can omit the execution of
  any command evaluating a Python based skip condition


1.1.0 (2018-01-16)
------------------

- Documentation updated (add new pytest play plugins)

- Support default payloads for command providers. Useful
  for HTTP authentication headers, common database settings


1.0.0 (2018-01-10)
------------------

- execute command accepts kwargs now

- execute command returns the command value now

- complete refactor of ``include`` provider (no
  backwards compatibility)

- add ``play_json.get_file_contents`` and removed
  ``data_getter`` fixture (no backwards compatibility)


0.3.1 (2018-01-04)
------------------

- play engine now logs commands to be executed and errors


0.3.0 (2018-01-04)
------------------

- you are able to update variables when executing commands

- you can extend ``pytest-play`` with new pluggable commands coming
  from third party packages thanks to setuptools entrypoints


0.2.0 (2018-01-02)
------------------

- no more open browser by default
  pytest-play is a generic test engine and it could be used for non UI tests too.

  So there is no need to open the browser for non UI tests (eg: API tests)


0.1.0 (2017-12-22)
------------------

- implement reusable steps (include scenario)

- minor documentation changes

0.0.1 (2017-12-20)
------------------

- First release
