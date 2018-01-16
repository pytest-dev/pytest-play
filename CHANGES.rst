Changelog
*********

1.1.0 (2018-01-16)
==================

- Documentation updated (add new pytest play plugins)

- Support default payloads for command providers. Useful
  for HTTP authentication headers, common database settings


1.0.0 (2018-01-10)
==================

- execute command accepts kwargs now

- execute command returns the command value now

- complete refactor of ``include`` provider (no
  backwards compatibility)

- add ``play_json.get_file_contents`` and removed
  ``data_getter`` fixture (no backwards compatibility)


0.3.1 (2018-01-04)
==================

- play engine now logs commands to be executed and errors


0.3.0 (2018-01-04)
==================

- you are able to update variables when executing commands

- you can extend ``pytest-play`` with new pluggable commands coming
  from third party packages thanks to setuptools entrypoints


0.2.0 (2018-01-02)
==================

- no more open browser by default
  pytest-play is a generic test engine and it could be used for non UI tests too.

  So there is no need to open the browser for non UI tests (eg: API tests)


0.1.0 (2017-12-22)
==================

- implement reusable steps (include scenario)

- minor documentation changes

0.0.1 (2017-12-20)
==================

- First release
