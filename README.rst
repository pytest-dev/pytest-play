===========
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

``pytest-play`` is a pytest_ plugin that let you **play** a json file describing some actions and assertions.
You can extend ``pytest-play`` with your own commands thanks to its pluggable architecture.

See at the bottom of the page the third party plugins that extends ``pytest-play``:

* `Third party pytest-play plugins`_

There are several testing frameworks. Sometimes they address just one single area testing needs: API testing only,
UI testing only and so on. It could be fine if you are testing a web only application like a CMS but if you are
dealing with a live IoT application you might need to simulate some device activities while testing your reactive UI (eg:
last positions or alarms updates), make some cross level checks (not only check the UI but also API for example),
quickly create some preconditions or contents needed by your UI scenarios for reactive
applications (I am on the assets page, there is not asset X, you create an asset X, the asset X automatically
appears in your asset listing), pure API testing (HTTP actions, assertions on response and database storage layer),
create always fresh test data on demand supporting manual testing activities or build some device simulator activities during
a demo or your exploratory testing sessions.

So pytest-play_ is a all in one testing framework: you can build automated test scenarios that combine different kind of
interactions for different testing levels.

With pytest-play_ you will be able to create automated test suites with no or very little Python knowledge: a
file ``test_XXX.json`` (e.g., ``test_something.json``. ``test_`` and ``.json`` matter) will be automatically
recognized and executed without having to touch any ``*.py`` module. You can run a single scenario
with ``pytest test_XXX.json`` or running the entire suite filtering by name or keyword markers.


How it works
------------

Depending on your needs and skills you can choose to use pytest-play programmatically
writing some Python code or following a Python-less approach.

Python-less (pure json)
=======================

Here you can see the contents of a ``pytest-play`` project without any Python files inside
containing a login scenario::

  $ tree
  .
  ├── env-ALPHA.yml
  ├── README.rst
  ├── test_login.ini
  └── test_login.json

with some default variables in a settings file specific for a target environment::  
  
  $ cat env-ALPHA.yml 
  pytest-play:
    base_url: https://www.yoursite.com

The test scenario with action and assertions::
  
  $ cat test_login.json
  {
      "steps": [
          {
              "comment": "visit base url",
              "type": "get",
              "url": "$base_url"
          },
          {
              "comment": "click on login link",
              "locator": {
                  "type": "id",
                  "value": "personaltools-login"
              },
              "type": "clickElement"
          },
          {
              "comment": "provide a username",
              "locator": {
                  "type": "id",
                  "value": "__ac_name"
              },
              "text": "$username",
              "type": "setElementText"
          },
          {
              "comment": "provide a password",
              "locator": {
                  "type": "id",
                  "value": "__ac_password"
              },
              "text": "$password",
              "type": "setElementText"
          },
          {
              "comment": "click on login submit button",
              "locator": {
                  "type": "css",
                  "value": ".pattern-modal-buttons > input[name=submit]"
              },
              "type": "clickElement"
          },
          {
              "comment": "wait for page loaded",
              "locator": {
                  "type": "css",
                  "value": ".icon-user"
              },
              "type": "waitForElementVisible"
          }
      ]
  }

Some optional metadata for each json scenario. In this case we have one or more markers so
you can filter tests to be executed invoking pytest with marker expressions. There is an
example of test parametrization too.
So the same ``test_login.json`` scenario will be executed 3 times with different
decoupled test data::

  $ cat test_login.ini
  [pytest]
  markers =
      login
  test_data =
      {"username": "siteadmin", "password": "siteadmin"}
      {"username": "editor", "password": "editor"}
      {"username": "reader", "password": "reader"}

You can see a basic example here:

* https://github.com/davidemoro/pytest-play-plone-example

Programmatically
================

You can invoke pytest-play programmatically too. 

You can define a test ``test_login.py`` like this::

  def test_login(play_json):
      data = play_json.get_file_contents(
          'my', 'path', 'etc', 'login.json')
      play_json.execute(data, extra_variables={})

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

    {
        "steps": [
            {"provider": "include", "type": "include", "path": "/some-path/included-scenario.json"},
            ... other commands ...
        ]
    }

You can create a variable for the base folder where your test scripts live.

Default commands
================

Some commands require many verbose options you don't want to repeat (eg: authentication headers for play_requests_).

Instead of replicating all the headers information you can initialize a ``pytest-play`` with the provider name as
key and as a value the default command you want to omit::

    {
        "steps": [{
            "provider": "python",
            "type": "store_variable",
            "name": "bearer",
            "expression": "'BEARER'"
        },
        {
            "provider": "python",
            "type": "store_variable",
            "name": "play_requests",
            "expression": "{'parameters': {'headers': {'Authorization': '$bearer'}}}"
        },
        {
             "provider": "play_requests",
             "type": "GET",
             "comment": "this is an authenticated request!",
             "url": "$base_url"
        }
    }

Store variables
===============

You can store a pytest-play_ variables::

    {
     'provider': 'python',
     'type': 'store_variable',
     'expression': '1+1',
     'name': 'foo'
    }

Make a Python assertion
=======================

You can make an assertion based on a Python expression::

    {
     'provider': 'python',
     'type': 'assert',
     'expression': 'variables["foo"] == 2'
    }

Sleep
=====

Sleep for a given amount of seconds::

    {
     'provider': 'python',
     'type': 'sleep',
     'seconds': 2
    }

Exec a Python expresssion
=========================

You can execute a Python expression::

    {
     'provider': 'python',
     'type': 'exec',
     'expression': '1+1'
    }

Wait until condition
====================

The ``wait_until_not`` command waits until the wait expression is False::

    {
     'provider': 'python',
     'type': 'wait_until_not',
     'expression': 'variables["expected_id"] is not None and variables["expected_id"][0] == $id',
     'timeout': 5,
     'poll': 0.1,
     'subcommands': [{
         'provider': 'play_sql',
         'type': 'sql',
         'database_url': 'postgresql://$db_user:$db_pwd@$db_host/$db_name',
         'query': 'SELECT id FROM table WHERE id=$id ORDER BY id DESC;',
         'variable': 'expected_id',
         'expression': 'results.first()'
     }]
    }

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

    play_json.execute_command({
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


Conditional commands (Python)
=============================

You can skip any command evaluating a Python based skip condition
like the following::

    {
      "provider": "include",
      "type": "include",
      "path": "/some-path/assertions.json",
      "skip_condition": "variables['cassandra_assertions'] is True"
    }


Browser based commands
----------------------

Browser based commands here.
``pytest-play`` supports by default browser interactions. For example it can be used for running selenium splinter_ scenarios driving your browser for your UI test or system tests.

``pytest-play`` is also your friend when page object approach (considered best practice) is not possible. For example:

* limited time, and/or
* lack of programming skills

Instead if you are interested in a page object pattern have a look at pypom_form_ or pypom_.

``pytest-play`` supports automatic waiting that should help to keep your tests more reliable with implicit waits before
moving on. By default it waits for node availability and visibility but it supports also some wait commands and
wait until a given Javascript expression is ok. So it is at the same time user friendly and flexible.

 
Conditional commands (Javascript)
=================================

Based on a browser level expression (Javascript)::

    {
      "type": "clickElement",
      "locator": {
           "type": "css",
           "value": "body"
           },
      "condition": "'$foo' === 'bar'"
    }


Supported locators
==================

Supported selector types:

* css
* xpath
* tag
* name
* text
* id
* value

Open a page
===========

With parametrization::

    {
      "type": "get",
      "url": "$base_url"
    }

or with a regular url::

    {
      "type": "get",
      "url": "https://google.com"
    }

Pause
=====

This command invokes a javascript expression that will
pause the execution flow of your commands::


    {
      "type": "pause",
      "waitTime": 1500
    }

If you need a pause/sleep for non UI tests you can use the
``sleep`` command provided by the play_python_ plugin.

Click an element
================
::

    {
      "type": "clickElement",
      "locator": {
           "type": "css",
           "value": "body"
           }
    }

Fill in a text
==============
::

    {
      "type": "setElementText",
      "locator": {
         "type": "css",
         "value": "input.title"
         },
      "text": "text value"
    }

Interact with select input elements
===================================

Select by label::

    {
      "type": "select",
      "locator": {
           "type": "css",
           "value": "select.city"
      },
      "text": "Turin"
    }

or select by value::

    {
      "type": "select",
      "locator": {
           "type": "css",
           "value": "select.city"
      },
      "value": "1"
    }

Eval a Javascript expression
============================

::

    {
      "type": "eval",
      "script": "alert("Hello world!")"
    }

Create a variable starting from a Javascript expression
=======================================================

The value of the Javascript expression will be stored in
``pytest_play.variables`` under the name ``count``::

    {
      "type": "storeEval",
      "variable": "count",
      "script": "document.getElementById('count')[0].textContent"
    }

Assert if a Javascript expression matches
=========================================

If the result of the expression does not match an ``AssertionError``
will be raised and the test will fail::

    {
      "type": "verifyEval",
      "value": "3",
      "script": "document.getElementById('count')[0].textContent"
    }

Verify that the text of one element contains a string
=====================================================

If the element text does not contain the provided text an
``AssertionError`` will be raised and the test will fail::

    {
      "type": "verifyText",
      "locator": {
         "type": "css",
         "value": ".my-item"
      },
      "text": "a text"
    }

Send keys to an element
=======================

All ``selenium.webdriver.common.keys.Keys`` are supported::

    {
      "type": "sendKeysToElement",
      "locator": {
         "type": "css",
         "value": ".confirm"
      },
      "text": "ENTER"
    }


Supported keys::

    KEYS = [
        'ADD', 'ALT', 'ARROW_DOWN', 'ARROW_LEFT', 'ARROW_RIGHT',
        'ARROW_UP', 'BACKSPACE', 'BACK_SPACE', 'CANCEL', 'CLEAR',
        'COMMAND', 'CONTROL', 'DECIMAL', 'DELETE', 'DIVIDE',
        'DOWN', 'END', 'ENTER', 'EQUALS', 'ESCAPE', 'F1', 'F10',
        'F11', 'F12', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
        'F9', 'HELP', 'HOME', 'INSERT', 'LEFT', 'LEFT_ALT',
        'LEFT_CONTROL', 'LEFT_SHIFT', 'META', 'MULTIPLY',
        'NULL', 'NUMPAD0', 'NUMPAD1', 'NUMPAD2', 'NUMPAD3',
        'NUMPAD4', 'NUMPAD5', 'NUMPAD6', 'NUMPAD7', 'NUMPAD8',
        'NUMPAD9', 'PAGE_DOWN', 'PAGE_UP', 'PAUSE', 'RETURN',
        'RIGHT', 'SEMICOLON', 'SEPARATOR', 'SHIFT', 'SPACE',
        'SUBTRACT', 'TAB', 'UP',
    ]

Wait until a Javascript expression matches
==========================================

Wait until the given expression matches or raise a 
``selenium.common.exceptions.TimeoutException`` if takes too time.

At this time of writing there is a global timeout (20s) but in future releases
you will be able to override it on command basis::

    {
      "type": "waitUntilCondition",
      "script": "document.body.getAttribute("class") === 'ready'"
    }

Wait for element present in DOM
===============================

Present::

    {
      "type": "waitForElementPresent",
      "locator": {
         "type": "css",
         "value": "body"
      }
    }

or not present::

    {
      "type": "waitForElementPresent",
      "locator": {
         "type": "css",
         "value": "body"
      },
      "negated": true
    }

Wait for element visible
========================

Visible::

    {
      "type": "waitForElementVisible",
      "locator": {
         "type": "css",
         "value": "body"
      }
    }

or not visible::

    {
      "type": "waitForElementVisible",
      "locator": {
         "type": "css",
         "value": "body"
      },
      "negated": true
    }

Assert element is present in DOM
================================

An ``AssertionError`` will be raised if assertion fails.

Present::

    {
      "type": "assertElementPresent",
      "locator": {
         "type": "css",
         "value": "div.elem"
         }
    }

or not present::

    {
      "type": "assertElementPresent",
      "locator": {
         "type": "css",
         "value": "div.elem"
         },
      "negated": true
    }

Assert element is visible
=========================

An ``AssertionError`` will be raised if assertion fails.

Present::

    {
      "type": "assertElementVisible",
      "locator": {
         "type": "css",
         "value": "div.elem"
         }
    }

or not present::

    {
      "type": "assertElementVisible",
      "locator": {
         "type": "css",
         "value": "div.elem"
         },
      "negated": true
    }


How to install pytest-play
--------------------------

You can see ``pytest-play`` in action creating a pytest project
using the cookiecutter-qa_ scaffolding tool:

* play.json_
* test_play.py_


This is the easiest way, otherwise you'll need to setup a pytest
project by your own and install ``pytest-play``.

pytest-play is pluggable and extensible
---------------------------------------

``pytest-play`` has a pluggable architecture and you can extend it.

For example you might want to support your own commands, support non UI
commands like making raw POST/GET/etc calls, simulate IoT devices
activities, provide easy interaction with complex UI widgets like
calendar widgets and so on.

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

JSON files metadata
-------------------

You can describe a scenario in pure JSON. You can also add some scenario metadata for
a ``test_XXX.json`` creating a ``test_XXX.ini`` file::

    [pytest]
    markers =
        marker1
        marker2
    test_data =
        {"username": "foo"}
        {"username": "bar"}

Option details:

* ``markers``, you can decorate your scenario with one or more markers. You can use them
  in pytest command line for filtering scenarios to be executed thanks to marker
  expressions like ``-m "marker1 and not slow"``

* ``test_data``, enables parametrization of arguments for a json scenario. For example
  if test data provides 2 json objects, your test scenario will be executed twice

New options will be added in the next feature (e.g., skip scenarios, xfail, xpass, etc).


Articles and talks
------------------

Articles:

* `Davide Moro: Hello pytest-play!`_

Talks:

* `Serena Martinetti @ Pycon9 - Florence: Integration tests ready to use with pytest-play`_ 


Third party pytest-play plugins
-------------------------------

* play_mqtt_, ``pytest-play`` plugin for MQTT support. Thanks to ``play_mqtt``
  you can test the integration between a mocked IoT device that sends
  commands on MQTT and a reactive web application with UI checks.

  You can also build a simulator that generates messages for you.

* play_requests_, ``pytest-play`` plugin driving the famous Python ``requests``
  library for making ``HTTP`` calls.

* play_sql_, ``pytest-play`` support for SQL expressions and assertions

* play_cassandra_, ``pytest-play`` support for Cassandra expressions and assertions

* play_dynamodb_, ``pytest-play`` support for AWS DynamoDB queries and assertions

* play_websocket_, ``pytest-play`` support for websockets

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
.. _`play.json`: https://github.com/davidemoro/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/data/play.json
.. _`test_play.py`: https://github.com/davidemoro/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/test_play.py
.. _`play_mqtt`: https://github.com/davidemoro/play_mqtt
.. _`play_python`: https://github.com/davidemoro/play_python
.. _`play_requests`: https://github.com/davidemoro/play_requests
.. _`play_sql`: https://github.com/davidemoro/play_sql
.. _`play_cassandra`: https://github.com/davidemoro/play_cassandra
.. _`play_dynamodb`: https://github.com/davidemoro/play_dynamodb
.. _`play_websocket`: https://github.com/davidemoro/play_websocket
.. _`RestrictedPython`: https://github.com/zopefoundation/RestrictedPython
.. _`Serena Martinetti @ Pycon9 - Florence: Integration tests ready to use with pytest-play`: https://www.pycon.it/conference/talks/integration-tests-ready-to-use-with-pytest-play
.. _`Davide Moro: Hello pytest-play!`: http://davidemoro.blogspot.it/2018/04/hello-pytest-play.html
