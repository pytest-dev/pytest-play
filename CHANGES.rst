Changelog
=========

2.3.0 (2019-04-05)
------------------

Features and improvements:

- ``wait_until`` and ``wait_until_not`` now accept commands with no ``sub_commands`` property

- implement new ``while`` command in python provider (while expression is true)

2.2.2 (2019-03-29)
------------------

Minor changes:

- remove internal property parameter on engine

Bugfix:

- add compatibility with ``pytest-repeat``'s ``--count`` command line option

Documentation:

- mention how to generate dynamic values using ``{! expr !}`` expressions
  (e.g., dynamic payloads in REST or MQTT without having to store variables
  when not needed)


2.2.1 (2019-03-19)
------------------

Minor changes:

- add ``int`` and ``float`` builtins available in Python expressions

- make python expressions more flexible for future improvements (internal change that doesn't
  affect compatibility)

Bugfix:

- fix ``--setup-plan`` invokation

Documentation:

- add more examples (bzt/Taurus and performance tests using pytest-play)


2.2.0 (2019-03-01)
------------------

- ``statsd`` integration (optional requirement) for advanced test metrics using statsd/graphite.
  If you install pytest play with the optional statsd support with ``pytest-play[statsd]``
  you will get the additional dependency ``statsd`` client and you can use the same cli
  options defined by the ``pytest-statsd`` plugin (e.g.,
  ``--stats-d [--stats-prefix myproject --stats-host http://myserver.com --stats-port 3000]``).

  Note well: despite the above cli options are the same defined by the ``pytest-statsd`` plugin,
  at this time of writing ``pytest-statsd`` is not a ``pytest-play`` dependency
  so you won't get stats about number of failures, passing, etc but only stats tracked by
  ``pytest-play``. If you need them you can install ``pytest-statsd`` (it plays well with ``pytest-play``)

2.1.0 (2019-02-22)
------------------

Features:

- support junit xml generation file with ``system-out`` element for
  each test case execution (pytest ``--junit-xml`` option).
  ``system-out`` will tracked by default in junit report unless you use
  the ``--capture=no`` or its alias ``-s``

- track ``_elapsed`` time for each executed command ``--junit-xml`` report
  if ``system-out`` is enabled

- track ``pytest`` custom properties in ``--junit-xml`` report for monitoring
  and measure what is important to you. For example you can track as key metric
  the time of the time occurred between the end of the previous action and
  the completion of the following. Basically you can track under the ``property_name``
  `load_login` key the time occurred between the click on the submit button
  and the end of the current command (e.g., click on the menu or text input
  being able to receive text) using a machine interpretable format.

  The ``property_name`` value elapsed time will be available as standard ``pytest-play``
  variable so that you can make additional assertions

- after every command execution a ``pytest-play`` variable will be added/updated
  reporting the elapsed time (accessible using ``variables['_elapsed']``).

  So be aware that the ``_elapsed`` variable name should be considered as a special
  variable and so you should not use this name for storing variables

- improve debug in case of failed assertions or errored commands. Logged variables
  dump in standard logs and ``system-out`` reporting if available

- improve debuggability in case of assertion errors (log failing expression)

- added a new ``metrics`` provider that let you track custom metrics in conjunction
  with ``--junit-xml`` option. You can track in a machine readable format response
  times, dynamic custom expressions, time that occurs between different commands
  (e.g., measure the time needed after a login to interact with the page, time before
  an asynchronous update happens and so on). Under the ``metrics`` provider you'll
  find the ``record_property``, ``record_elapsed``, ``record_elapsed_start``  and
  ``record_elapsed_stop`` commands

Documentation:

- minor documentation changes

- add more examples


2.0.2 (2019-02-06)
------------------

Documentation:

- more examples

- fix documentation bug on README (example based on selenium with missing ``provider: selenium``)


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
