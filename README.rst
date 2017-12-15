===========
pytest-play
===========


.. image:: https://travis-ci.org/tierratelematics/pytest-play.svg?branch=develop
    :target: https://travis-ci.org/tierratelematics/pytest-play
    :alt: See Build Status on Travis CI

.. image:: https://readthedocs.org/projects/pytest-play/badge/?version=latest
          :target: http://pytest-play.readthedocs.io

.. image:: https://codecov.io/gh/tierratelematics/pytest-play/branch/develop/graph/badge.svg
          :target: https://codecov.io/gh/tierratelematics/pytest-play

``pytest-play`` is a pytest_ plugin that let you **play** a json file containing previously
recorded selenium splinter_ actions driving your browser for your UI test.

``pytest-play`` is your friend when page object approach (considered best practice) is not possible. For example:

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
    				"type": "css selector",
    				"value": "input[name=\"email\"]"
    			},
    			"text": "$root_name"
    		},
    		{
    			"type": "setElementText",
    			"locator": {
    				"type": "css selector",
    				"value": "input[name=\"password\"]"
    			},
    			"text": "$root_pwd"
    		},
    		{
    			"type": "clickElement",
    			"locator": {
    				"type": "css selector",
    				"value": ".label-submit"
    			}
    		},
    		{
    			"type": "waitForElementPresent",
    			"locator": {
    				"type": "css selector",
    				"value": ".logged"
    			}
    		},
    		{
    			"type": "assertElementPresent",
    			"locator": {
    				"type": "css selector",
    				"value": ".user-info"
    			}
    		}
    	]
    }

you define a test ``test_login.py`` like this::

    def test_login(play_json):
        data = data_getter('/my/path/etc', 'login.json')
        play_json.execute(data)

you get things moving on your browser!

Commands syntax
===============

Project status is pre-alpha so commands could change and the
following list will be extended.

Conditional commands
--------------------
::

    {
      "type": "clickElement",
      "locator": {
           "type": "css selector",
           "value": "body"
           },
      "condition": "'$foo' === 'bar'"
    }

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
      "waitTime": "1500"
    }

Click an element
----------------
::

    {
      "type": "clickElement",
      "locator": {
           "type": "css selector",
           "value": "body"
           }
    }

Fill in a text
--------------
::

    {
      "type": "setElementText",
      "locator": {
         "type": "css selector",
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
           "type": "css selector",
           "value": "select.city"
      },
      "text": "Turin"
    }

or select by value::

    {
      "type": "select",
      "locator": {
           "type": "css selector",
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
         "type": "css selector",
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
         "type": "css selector",
         "value": ".confirm"
      },
      "text": "ENTER"
    }

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
