Usage (docker required)::

    $ docker run --rm -it -v $(pwd):/src davidemoro/pytest-play --stats-d --stats-prefix play --splinter-webdriver remote --splinter-remote-url http://USERNAME:ACCESSKEY@hub.browserstack.com:80/wd/hub

Alternatively you can use the ``--splinter-webdriver firefox|chrome`` assuming that you already installed
``geckodriver`` or ``chromedriver``.
