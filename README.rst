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

    def test_login(play_json, data_getter):
        data = data_getter('/my/path/etc', 'login.json')
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
::

    {
      "type": "pause",
      "waitTime": 1500
    }

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
            {"provider": "included-scenario.json", "type": "include"},
            ... other commands ...
        ]
    }

registering ``included-scenario.json``'s contents as follows::

    @pytest.fixture(autouse=True)
    def included_scenario(play_json, data_getter, data_base_path):
        data = data_getter(data_base_path, 'included-scenario.json')
        play_json.register_steps(
            data, 'included-scenario.json')


This way other json files will be able to include the ``included-scenario.json`` file.


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

    command = {'type': 'print', 'provider': 'newprovider'}

You just have to implement a command provider::


    class NewProvider(object):
        def __init__(self, engine):
            self.engine = engine

        def this_is_not_a_command(self):
            """ Commands should be command_ prefixed """

        def command_print(self, command):
            print(command)

        def command_yetAnotherCommand(self, command):
            print(command)

and register your new provider::

    import pytest


    @pytest.fixture(autouse=True)
    def newprovider(play_json):
        play_json.register_command_provider(NewProvider, 'newprovider')

You can define new providers also for non UI commands. For example publish MQTT
messages simulating IoT device activities for integration tests.


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
