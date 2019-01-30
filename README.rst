pytest-play
===========

.. image:: https://travis-ci.org/pytest-dev/pytest-play.svg?branch=master
    :target: https://travis-ci.org/pytest-dev/pytest-play
    :alt: See Build Status on Travis CI

.. image:: https://readthedocs.org/projects/pytest-play/badge/?version=latest
    :target: http://pytest-play.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/pytest-dev/pytest-play/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pytest-dev/pytest-play

``pytest-play`` is a codeless, generic, pluggable and extensible **automation tool**,
not necessarily **test automation** only, based on the fantastic pytest_ test framework
that let you define and execute YAML_ files containing scripts or test scenarios
through actions and assertions that can be implemented and managed even by **non technical users**:

* automation (not necessarily test automation). You can build a set of actions on a single file (e.g,
  call a JSON based API endpoint, perform an action if a condition matches) or a test automation
  project with many test scenarios.

  For example you can create always fresh test data on demand supporting
  manual testing activities, build a live simulator and so on

* codeless, or better almost codeless. If you have to write assertions against action results or some
  conditional expressions you need a very basic knowledge of Python or Javascript expressions
  with a smooth learning curve (something like ``variables['foo'] == 'bar'``)

* generic. It is not yet again another automation tool for browser automation only, API only, etc.
  You can drive a browser, perform some API calls, make database queries and/or make assertions
  using the same tool for different technologies

  So there are several free or not free testing frameworks or automation tools and many times
  they address just one single area testing needs and they are not extensible: API testing only,
  UI testing only and so on. It could be fine if you are testing a web
  only application like a CMS but if you are dealing with a reactive IoT application you might something more,
  make cross actions or cross checks against different systems or build something of more complex upon
  ``pytest-play``

* powerful. It is not yet again another test automation tool, it only extends the pytest_ framework
  with another paradigm and inherits a lot of good stuff (test data decoupled by test implementation
  that let you write once and executed many times the same scenario thanks to native parametrization
  support, reporting, integration with test management tools, many useful command line options, browsers and
  remote Selenium grids integration, etc)

* pluggable and extensible. Let's say you need to interact with a system not yet supported by a ``pytest-play``
  plugin, you can write by your own or pay someone for you. In addition there is a scaffolding tool that
  let you implement your own command: https://github.com/davidemoro/cookiecutter-play-plugin
  
* easy to use. Why YAML? Easy to read, easy to write, simple and standard syntax, easy to be validated and
  no parentheses hell. Despite there are no recording tools (not yet) for browser interaction or API calls, the
  documentation based on very common patterns let you copy, paste and edit command by command with no pain

* free software. It's an open source project based on the large and friendly pytest_ community

* easy to install. The only prerequisite is Docker thanks to the ``davidemoro/pytest-play`` Docker Hub container.
  Or better, with docker, no installation is required: you just need to type the following command
  ``docker run -i --rm -v $(pwd):/src davidemoro/pytest-play`` inside your project folder
  See https://hub.docker.com/r/davidemoro/pytest-play

See at the bottom of the page the third party plugins that extends ``pytest-play``:

* `Third party pytest-play plugins`_

How it works
------------

Depending on your needs and skills you can choose to use pytest-play programmatically
writing some Python code or following a Python-less approach.

As said before with pytest-play_ you will be able to create codeless scripts or test scenarios
with no or very little Python knowledge: a file ``test_XXX.yml`` (e.g., ``test_something.yml``,
where ``test_`` and ``.yml`` matter) will be automatically recognized and executed without having
to touch any ``*.py`` module. 

You can run a single scenario with ``pytest test_XXX.yml`` or running the entire suite filtering
by name or keyword markers.

Despite ``pytest-play`` was born with native support for JSON format, ``pytest-play``>=2.0 versions will support
YAML only for improved usability.

Python-less (pure YAML)
=======================

Here you can see the contents of a ``pytest-play`` project without any Python files inside
containing a login scenario::

  $ tree
  .
  ├── env-ALPHA.yml    (OPTIONAL)
  └── test_login.yml

and you might have some global variables in a settings file specific for a target environment::  
  
  $ cat env-ALPHA.yml 
  pytest-play:
    base_url: https://www.yoursite.com

The test scenario with action, assertions and optional metadata
(play_selenium_ external plugin needed)::
  
  $ cat test_login.yml
  ---
  markers:
    - login
  test_data:
    - username: siteadmin
      password: siteadmin
    - username: editor
      password: editor
    - username: reader
      password: reader
  ---
  - comment: visit base url
    type: get
    url: "$base_url"
  - comment: click on login link
    locator:
      type: id
      value: personaltools-login
    type: clickElement
  - comment: provide a username
    locator:
      type: id
      value: __ac_name
    text: "$username"
    type: setElementText
  - comment: provide a password
    locator:
      type: id
      value: __ac_password
    text: "$password"
    type: setElementText
  - comment: click on login submit button
    locator:
      type: css
      value: ".pattern-modal-buttons > input[name=submit]"
    type: clickElement
  - comment: wait for page loaded
    locator:
      type: css
      value: ".icon-user"
    type: waitForElementVisible

The first optional YAML document contains some metadata with keywords aka ``markers``
so you can filter tests to be executed invoking pytest with marker expressions,
decoupled test data, etc.

The same ``test_login.yml`` scenario will be executed 3 times with different
decoupled test data ``test_data`` defined inside its first optional YAML
document (the block between the 2 ``---`` lines).

So write once and execute many times with different test data!

You can see a hello world example here:

* https://github.com/davidemoro/pytest-play-plone-example

As told before the metadata document is optional so you might have 1 or 2
documents in your YAML file. You can find more info about `Metadata format`_.

Here you can see the same example without the metadata section for sake of
completeness::

  ---
  - comment: visit base url
    type: get
    url: "http://YOURSITE"
  - comment: click on login link
    locator:
      type: id
      value: personaltools-login
    type: clickElement
  - comment: provide a username
    locator:
      type: id
      value: __ac_name
    text: "YOURUSERNAME"
    type: setElementText
  - comment: provide a password
    locator:
      type: id
      value: __ac_password
    text: "YOURPASSWORD"
    type: setElementText
  - comment: click on login submit button
    locator:
      type: css
      value: ".pattern-modal-buttons > input[name=submit]"
    type: clickElement
  - comment: wait for page loaded
    locator:
      type: css
      value: ".icon-user"
    type: waitForElementVisible

Programmatically
================

You can invoke pytest-play programmatically too. 

You can define a test ``test_login.py`` like this::

  def test_login(play):
      data = play.get_file_contents(
          'my', 'path', 'etc', 'login.yml')
      play.execute_raw(data, extra_variables={})

Or this programmatical approach might be used if you are
implementing BDD based tests using ``pytest-bdd``.

Core commands
-------------

pytest-play_ provides some core commands that let you:

* write simple Python assertions, expressions and variables

* reuse steps including other test scenario scripts

* provide a default command template for some particular providers
  (eg: add by default HTTP authentication headers for all requests)

* a generic wait until machinery. Useful for waiting for an
  observable asynchronous event will complete its flow before
  proceeding with the following commands that depends on the previous
  step completion

You can write restricted Python expressions and assertions based on the ``RestrictedPython`` package.

RestrictedPython_ is a tool that helps to define a subset of the Python
language which allows to provide a program input into a trusted environment.
RestrictedPython is not a sandbox system or a secured environment, but it helps
to define a trusted environment and execute untrusted code inside of it.

See:

* https://github.com/zopefoundation/RestrictedPython

How to reuse steps
==================

You can split your commands and reuse them using the ``include`` command avoiding
duplication::

    - provider: include
      type: include
      path: "/some-path/included-scenario.yml"


You can create a variable for the base folder where your test scripts live.

Default commands
================

Some commands require many verbose options you don't want to repeat (eg: authentication headers for play_requests_).

Instead of replicating all the headers information you can initialize a ``pytest-play`` with the provider name as
key and as a value the default command you want to omit (this example neets the external plugin play_selenium_)::

    - provider: python
      type: store_variable
      name: bearer
      expression: "'BEARER'"
    - provider: python
      type: store_variable
      name: play_requests
      expression: "{'parameters': {'headers': {'Authorization': '$bearer'}}}"
    - provider: play_requests
      type: GET
      comment: this is an authenticated request!
      url: "$base_url"


Store variables
===============

You can store a pytest-play_ variables::

    - provider: python
      type: store_variable
      expression: "1+1"
      name: foo

Make a Python assertion
=======================

You can make an assertion based on a Python expression::

    - provider: python
      type: assert
      expression: variables['foo'] == 2

Sleep
=====

Sleep for a given amount of seconds::

    - provider: python
      type: sleep
      seconds: 2

Exec a Python expresssion
=========================

You can execute a Python expression::

    - provider: python
      type: exec
      expression: "1+1"

Wait until condition
====================

The ``wait_until_not`` command waits until the wait expression is `False` (this example
contains a SQL query so the external plugin called play_sql_ is needed plus
the appropriate SQL driver depending on database type)::

    - provider: python
      type: wait_until_not
      expression: variables['expected_id'] is not None and variables['expected_id'][0] == $id
      timeout: 5
      poll: 0.1
      subcommands:
      - provider: play_sql
        type: sql
        database_url: postgresql://$db_user:$db_pwd@$db_host/$db_name
        query: SELECT id FROM table WHERE id=$id ORDER BY id DESC;
        variable: expected_id
        expression: results.first()

assuming that the subcommand updates the execution results updating a ``pytest-play``
variable (eg: ``expected_id``) where tipically the ``$id`` value comes
from a previously executed command that causes an asynchrounous update on a relational
database soon or later (eg: a play_requests_ command making a ``HTTP POST`` call
or a ``MQTT`` message coming from a simulated IoT device with play_mqtt_).

The wait command will try (and retry) to execute the subcommand with a poll frequency
``poll`` (default: 0.1 seconds) until the provided ``timeout`` expressed
in seconds expires or an exception occurs.

You can use the opposite command named ``wait_until`` that waits until the wait
expression is not False.

Loop commands
=============

You can repeat a group of subcommands using a variable as a counter. Assuming you
have defined a ``countdown`` variable with 10 value, the wait until command will
repeat the group of commands for 10 times::

    play.execute_command({
        'provider': 'python',
        'type': 'wait_until',
        'expression': 'variables["countdown"] == 0',
        'timeout': 0,
        'poll': 0,
        'sub_commands': [{
            'provider': 'python',
            'type': 'store_variable',
            'name': 'countdown',
            'expression': 'variables["countdown"] - 1'
        }]
    })

or::

    - provider: python
      type: wait_until
      expression: variables['countdown'] == 0
      timeout: 0
      poll: 0
      sub_commands:
      - provider: python
        type: store_variable
        name: countdown
        expression: variables['countdown'] - 1


Conditional commands (Python)
=============================

You can skip any command evaluating a Python based skip condition
like the following::

    - provider: include
      type: include
      path: "/some-path/assertions.yml"
      skip_condition: variables['cassandra_assertions'] is True


Browser based commands
----------------------

The ``pytest-play`` core no more includes browser based commands. Moved to play_selenium_
external plugin.

pytest-play is pluggable and extensible
---------------------------------------

``pytest-play`` has a pluggable architecture and you can extend it.

For example you might want to support your own commands, support non UI
commands like making raw POST/GET/etc calls, simulate IoT devices
activities, provide easy interaction with complex UI widgets like
calendar widgets, send commands to a device using the serial port implementing
a binary protocol and so on.

How to register a new command provider
======================================

Let's suppose you want to extend pytest-play with the following command::

    command = {'type': 'print', 'provider': 'newprovider', 'message': 'Hello, World!'}

You just have to implement a command provider::

    from pytest_play.providers import BaseProvider

    class NewProvider(BaseProvider):

        def this_is_not_a_command(self):
            """ Commands should be command_ prefixed """

        def command_print(self, command):
            print(command['message'])

        def command_yetAnotherCommand(self, command):
            print(command)

and register your new provider in your ``setup.py`` adding an entrypoint::

    entry_points={
        'playcommands': [
            'print = your_package.providers:NewProvider',
        ],
    },

You can define new providers also for non UI commands. For example publish MQTT
messages simulating IoT device activities for integration tests.

If you want you can generate a new command provider thanks to:

* https://github.com/davidemoro/cookiecutter-play-plugin

Metadata format
---------------

You can also add some scenario metadata placing another YAML document on top of the scenario
defined on the ``test_XXX.yml`` with the following format::

    ---
    markers:
      - marker1
      - marker2
    test_data:
      - username: foo
      - username: bar
    ---
    # omitted scenario steps in this example...

Option details:

* ``markers``, you can decorate your scenario with one or more markers. You can use them
  in pytest command line for filtering scenarios to be executed thanks to marker
  expressions like ``-m "marker1 and not slow"``

* ``test_data``, enables parametrization of your decoupletd test data and let you execute
  the same scenario many times. For example
  the example above will be executed twice (one time with "foo" username and another time
  with "bar")

New options will be added in the next feature (e.g., skip scenarios, xfail, xpass, etc).


Articles and talks
------------------

Articles:

* `Davide Moro: Hello pytest-play!`_

Talks:

* `Serena Martinetti @ Pycon9 - Florence: Integration tests ready to use with pytest-play`_ 


Third party pytest-play plugins
-------------------------------

* play_selenium_, ``pytest-play`` plugin driving browsers using Selenium/Splinter
  under the hood. Selenium grid compatible and implicit auto wait actions
  for more robust scenarios with less controls.

* play_requests_, ``pytest-play`` plugin driving the famous Python ``requests``
  library for making ``HTTP`` calls.

* play_sql_, ``pytest-play`` support for SQL expressions and assertions

* play_cassandra_, ``pytest-play`` support for Cassandra expressions and assertions

* play_dynamodb_, ``pytest-play`` support for AWS DynamoDB queries and assertions

* play_websocket_, ``pytest-play`` support for websockets

* play_mqtt_, ``pytest-play`` plugin for MQTT support. Thanks to ``play_mqtt``
  you can test the integration between a mocked IoT device that sends
  commands on MQTT and a reactive web application with UI checks.

  You can also build a simulator that generates messages for you.


Feel free to add your own public plugins with a pull request!


Twitter
-------

``pytest-play`` tweets happens here:

* `@davidemoro`_
 

.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pypom_form`: http://pypom-form.readthedocs.io/en/latest/
.. _`splinter`: https://splinter.readthedocs.io/en/latest/
.. _`pypom`: http://pypom.readthedocs.io/en/latest/
.. _`@davidemoro`: https://twitter.com/davidemoro
.. _`cookiecutter-qa`: https://github.com/davidemoro/cookiecutter-qa
.. _`play.yml`: https://github.com/davidemoro/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/data/play.yml
.. _`test_play.py`: https://github.com/davidemoro/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/test_play.py
.. _`play_mqtt`: https://github.com/davidemoro/play_mqtt
.. _`play_selenium`: https://github.com/davidemoro/play_selenium
.. _`play_requests`: https://github.com/davidemoro/play_requests
.. _`play_sql`: https://github.com/davidemoro/play_sql
.. _`play_cassandra`: https://github.com/davidemoro/play_cassandra
.. _`play_dynamodb`: https://github.com/davidemoro/play_dynamodb
.. _`play_websocket`: https://github.com/davidemoro/play_websocket
.. _`RestrictedPython`: https://github.com/zopefoundation/RestrictedPython
.. _`Serena Martinetti @ Pycon9 - Florence: Integration tests ready to use with pytest-play`: https://www.pycon.it/conference/talks/integration-tests-ready-to-use-with-pytest-play
.. _`Davide Moro: Hello pytest-play!`: http://davidemoro.blogspot.it/2018/04/hello-pytest-play.html
.. _`YAML`: https://en.wikipedia.org/wiki/YAML
