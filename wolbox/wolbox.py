#!/usr/bin/env python3
"""
Wolbox

Author: Moritz Röhrich <moritz@ildefons.de>
"""

import flask
import wakeonlan

bp = flask.Blueprint("wolbox", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    """
    Blueprint route for /.
    """
    if flask.request.method == "POST":
        wake(flask.request.form["hostname"])
    return flask.render_template("wolbox/index.html",
                                 hosts=flask.current_app.config["HOST_LIST"])


@bp.route("/wake/<string:hostname>", methods=["POST"])
def wake(hostname):
    """
    """
    mac = get_mac(hostname)
    print("Waking: %s.%s (%s)" % (hostname,
                                  flask.current_app.config["DOMAIN"], mac))
    wakeonlan.send_magic_packet(mac)
    return flask.render_template("wolbox/index.html",
                                 hosts=flask.current_app.config["HOST_LIST"])


def get_mac(hostname):
    for h in flask.current_app.config["HOST_LIST"]:
        if h["hostname"] == hostname:
            return h["mac"]
    return "00:00:00:00:00:00"
