#!/usr/bin/env python3
"""
Author: Moritz Röhrich <moritz@ildefons.de>
"""

import os
import threading
import atexit
import flask

from wolbox import wolbox


SCAN_FREQ = 5
lock = threading.Lock()
scanner = threading.Thread()


def create_app(test_config=None):

    def interrupt():
        global scanner
        scanner.cancel()

    def scan():
        global scanner
        with lock:
            wolbox.discover()

        scanner = threading.Timer(SCAN_FREQ, scan, ())
        scanner.start()

    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_mapping()

    if test_config is None:
        app.config.from_pyfile("config.py", silent=False)
    else:
        app.config.update(test_config)

    app.config["SERVER_NAME"] = os.getenv("WOLBOX_URL",
                                          app.config["SERVER_NAME"])
    app.config["DOMAIN"] = os.getenv("WOLBOX_DOMAIN",
                                     app.config["DOMAIN"])
    app.config["SUBNET"] = os.getenv("WOLBOX_SUBNET",
                                     app.config["SUBNET"])
    global SCAN_FREQ
    SCAN_FREQ = os.getenv("WOLBOX_SCAN_FREQ",
                          app.config["SCAN_FREQ"])

    wolbox.subnet = app.config["SUBNET"]
    wolbox.hosts = app.config["HOST_LIST"]
    wolbox.domain = app.config["DOMAIN"]
    scan()
    atexit.register(interrupt)

    app.register_blueprint(wolbox.bp)
    app.add_url_rule("/", endpoint="index")

    return app
