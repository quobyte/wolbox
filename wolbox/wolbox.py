#!/usr/bin/env python3
"""
Wolbox

Author: Moritz Röhrich <moritz@ildefons.de>
"""

import flask
import nmap3
import wakeonlan

bp = flask.Blueprint("wolbox", __name__)

hosts = []
domain = ""
subnet = ""


@bp.route("/", methods=("GET", "POST"))
def index():
    """
    Blueprint route for /.
    """
    global hosts
    global domain
    if flask.request.method == "POST":
        wake(flask.request.form["hostname"])
    return flask.render_template("wolbox/index.html",
                                 hosts=hosts)


@bp.route("/wake/<string:hostname>", methods=["POST"])
def wake(hostname):
    global hosts
    global domain
    mac = get_mac(hostname)
    print("Waking: %s.%s (%s)" % (hostname, domain, mac))
    wakeonlan.send_magic_packet(mac)
    return flask.render_template("wolbox/index.html", hosts=hosts)


def get_mac(hostname):
    for h in flask.current_app.config["HOST_LIST"]:
        if h["hostname"] == hostname:
            return h["mac"]
    return "00:00:00:00:00:00"


def discover():
    global hosts
    global domain
    global subnet
    nmap = nmap3.NmapScanTechniques()
    discovered = nmap.nmap_ping_scan(subnet, args="--send-ip")

    for h in hosts:
        h["status"] = "Down"
    for d in discovered:
        if d == "stats" or d == "runtime":
            continue
        for h in hosts:
            fqdn = h["hostname"]+"."+domain
            hostinfo = discovered[d]["hostname"]
            discovered_host = next(iter(hostinfo), {"name": "none"})["name"]
            if fqdn.lower() == discovered_host.lower():
                h["status"] = "Up"
