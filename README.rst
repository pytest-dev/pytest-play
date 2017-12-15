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

Project status is pre-alpha so commands could change.

...

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
