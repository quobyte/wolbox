#!/usr/bin/env python3
"""
Author: Moritz Röhrich <moritz@ildefons.de>
"""

import os

import flask

from wolbox import wolbox


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = flask.Flask(__name__, instance_relative_config=False)
    app.config.from_mapping()

    if test_config is None:
        app.config.from_pyfile("config.py", silent=False)
    else:
        app.config.update(test_config)

    app.config["SERVER_NAME"] = os.getenv(
        "WOLBOX_URL", app.config["SERVER_NAME"]
    )

    app.register_blueprint(wolbox.bp)
    app.add_url_rule("/", endpoint="index")

    return app
