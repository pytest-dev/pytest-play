===========
pytest-play
===========


.. image:: https://travis-ci.org/tierratelematics/pytest-play.svg?branch=develop
    :target: https://travis-ci.org/tierratelematics/pytest-play
    :alt: See Build Status on Travis CI

.. image:: https://readthedocs.org/projects/pytest-play/badge/?version=latest
    :target: http://pytest-play.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/tierratelematics/pytest-play/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/tierratelematics/pytest-play

``pytest-play`` is a pytest_ plugin that let you **play** a json file describing some actions and assertions.
You can extend ``pytest-play`` with your own commands thanks to its pluggable architecture and by default it supports
browser interactions. For example it can be used for running previously recorded selenium splinter_ actions driving your
browser for your UI test.

See at the bottom of the page the third party plugins that extends ``pytest-play``.

``pytest-play`` is also your friend when page object approach (considered best practice) is not possible. For example:

* limited time, and/or
* lack of programming skills

Instead if you are interested in a page object pattern have a look at pypom_form_ or pypom_.

``pytest-play`` supports automatic waiting that should help to keep your tests more reliable with implicit waits before
moving on. By default it waits for node availability and visibility but it supports also some wait commands and
wait until a given Javascript expression is ok. So it is at the same time user friendly and flexible.


How it works
------------
Given a json file (eg: ``login.json``)::

    {
    	"steps": [
    		{
    			"type": "get",
    			"url": "$base_url"
    		},
    		{
    			"type": "setElementText",
    			"locator": {
    				"type": "css",
    				"value": "input[name=\"email\"]"
    			},
    			"text": "$root_name"
    		},
    		{
    			"type": "setElementText",
    			"locator": {
    				"type": "css",
    				"value": "input[name=\"password\"]"
    			},
    			"text": "$root_pwd"
    		},
    		{
    			"type": "clickElement",
    			"locator": {
    				"type": "css",
    				"value": ".label-submit"
    			}
    		},
    		{
    			"type": "waitForElementPresent",
    			"locator": {
    				"type": "css",
    				"value": ".logged"
    			}
    		},
    		{
    			"type": "assertElementPresent",
    			"locator": {
    				"type": "css",
    				"value": ".user-info"
    			}
    		}
    	]
    }

you define a test ``test_login.py`` like this::

    def test_login(play_json):
        data = play_json.get_file_contents(
            '/my/path/etc', 'login.json')
        play_json.execute(data)

you get things moving on your browser!

Commands syntax
===============

Project status is pre-alpha so commands could change and the
following list will be extended.

Some useful commands is missing, for example:

* url assertions

* text in page

* interaction with other input elements like radio buttons

Conditional commands
--------------------
::

    {
      "type": "clickElement",
      "locator": {
           "type": "css",
           "value": "body"
           },
      "condition": "'$foo' === 'bar'"
    }


Supported locators
------------------

Supported selector types:

* css
* xpath
* tag
* name
* text
* id
* value

Open a page
-----------

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
-----

This command invokes a javascript expression that will
pause the execution flow of your commands::


    {
      "type": "pause",
      "waitTime": 1500
    }

If you need a pause/sleep for non UI tests you can use the
``sleep`` command provided by the play_python_ plugin.

Click an element
----------------
::

    {
      "type": "clickElement",
      "locator": {
           "type": "css",
           "value": "body"
           }
    }

Fill in a text
--------------
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
-----------------------------------

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
----------------------------

::

    {
      "type": "eval",
      "script": "alert("Hello world!")"
    }

Create a variable starting from a Javascript expression
-------------------------------------------------------

The value of the Javascript expression will be stored in
``pytest_play.variables`` under the name ``count``::

    {
      "type": "storeEval",
      "variable": "count",
      "script": "document.getElementById('count')[0].textContent"
    }

Assert if a Javascript expression matches
-----------------------------------------

If the result of the expression does not match an ``AssertionError``
will be raised and the test will fail::

    {
      "type": "verifyEval",
      "value": "3",
      "script": "document.getElementById('count')[0].textContent"
    }

Verify that the text of one element contains a string
-----------------------------------------------------

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
-----------------------

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
------------------------------------------

Wait until the given expression matches or raise a 
``selenium.common.exceptions.TimeoutException`` if takes too time.

At this time of writing there is a global timeout (20s) but in future releases
you will be able to override it on command basis::

    {
      "type": "waitUntilCondition",
      "script": "document.body.getAttribute("class") === 'ready'"
    }

Wait for element present in DOM
-------------------------------

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
------------------------

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
--------------------------------

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
-------------------------

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

How to reuse steps
------------------

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
----------------

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
            "type": "exec",
            "expression": "variables.update({'play_requests': {'parameters': {'headers': {'Authorization': '$bearer'}}}})"
        },
        {
             "provider": "play_requests",
             "type": "GET",
             "comment": "this is an authenticated request!",
             "url": "$base_url"
        }
    }

How to install pytest-play
==========================

You can see ``pytest-play`` in action creating a pytest project
using the cookiecutter-qa_ scaffolding tool:

* play.json_
* test_play.py_


This is the easiest way, otherwise you'll need to setup a pytest
project by your own and install ``pytest-play``.

pytest-play is pluggable and extensible
=======================================

``pytest-play`` has a pluggable architecture and you can extend it.

For example you might want to support your own commands, support non UI
commands like making raw POST/GET/etc calls, simulate IoT devices
activities, provide easy interaction with complex UI widgets like
calendar widgets and so on.

How to register a new command provider
--------------------------------------

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

* https://github.com/tierratelematics/cookiecutter-play-plugin


Third party pytest-play plugins
===============================

* play_mqtt_, ``pytest-play`` plugin for MQTT support. Thanks to ``play_mqtt``
  you can test the integration between a mocked IoT device that sends
  commands on MQTT and a reactive web application with UI checks.

  You can also build a simulator that generates messages for you.

* play_python_, ``pytest-play`` plugin with restricted Python expressions and
  assertions and it is based on the RestrictedPython_ package.

* play_requests_, ``pytest-play`` plugin driving the famous Python ``requests``
  library for making ``HTTP`` calls.

* play_sql_, ``pytest-play`` support for SQL expressions and assertions

* play_cassandra_, ``pytest-play`` support for Cassandra expressions and assertions

* **play_selenium**, the ``pytest-play`` selenium commands for UI tests
  will be implemented on a brand new package named play_selenium

Feel free to add your own public plugins with a pull request!


Twitter
=======

``pytest-play`` tweets happens here:

* `@davidemoro`_
 

.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`file an issue`: https://github.com/tierratelematics/pytest-play/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pypom_form`: http://pypom-form.readthedocs.io/en/latest/
.. _`splinter`: https://splinter.readthedocs.io/en/latest/
.. _`pytest-splinter`: https://github.com/pytest-dev/pytest-splinter
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`pypom`: http://pypom.readthedocs.io/en/latest/
.. _`PyPI`: https://pypi.python.org/pypi
.. _`@davidemoro`: https://twitter.com/davidemoro
.. _`cookiecutter-qa`: https://github.com/tierratelematics/cookiecutter-qa
.. _`play.json`: https://github.com/tierratelematics/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/data/play.json
.. _`test_play.py`: https://github.com/tierratelematics/cookiecutter-qa/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/tests/functional/test_play.py
.. _`play_mqtt`: https://github.com/tierratelematics/play_mqtt
.. _`play_python`: https://github.com/tierratelematics/play_python
.. _`play_requests`: https://github.com/tierratelematics/play_requests
.. _`play_sql`: https://github.com/tierratelematics/play_sql
.. _`play_cassandra`: https://github.com/tierratelematics/play_cassandra
.. _`RestrictedPython`: https://github.com/zopefoundation/RestrictedPython
