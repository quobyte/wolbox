Wolbox - Small Web based Wake on LAN tool
=========================================

Wolbox is a small web based tool, that you can use to wake sleeping computers on
your LAN.

Set Up
------

Enter your network details in wolbox/config.py. Then either run

    $ ./run.sh

or run this on Docker with the provided dockerfile.

When running in Docker, use a command along the lines of:

    $ docker run --rm --net=host --security-opt no-new-privileges -p 8080:8080 wolbox

The `--net=host` is necessary to allow the magic packages to be properly sent.

Configuration
-------------

### `SERVER_NAME`

Set this to the FQDN of the host where you run this app.
You can also set this via the environment variable `WOLBOX_URL`.

### `DOMAIN`

Set this to the domain where the hosts that you want to wake live.
You can also set this via the environment variable `WOLBOX_DOMAIN`.

### `SUBNET`

Set this to the ip subnet in CIDR notation where the hosts that need waking
live.
You can also set this via the environment variable `WOLBOX_SUBNET`.

### `SCAN_FREQ`

Wolbox periodically scans the subnet to determine wether or not a host is
online. Set this to the period in seconds (e.g. 20 ==> scan every 20 secons).
You can also set this via the environment variable `WOLBOX_SCAN_FREQ`.
