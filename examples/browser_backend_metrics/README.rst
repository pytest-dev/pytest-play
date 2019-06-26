Usage (docker required)::

    docker run --rm -it -v $(pwd):/src davidemoro/pytest-play --splinter-webdriver remote --splinter-remote-url http://USER:KEY@hub.browserstack.com:80/wd/hub
