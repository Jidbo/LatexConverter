import re
import requests


class StatusCodeError(Exception):

    def __init__(self, expected, actual):
        super().__init__(self, "")

        self.expected = expected
        self.actual = actual

    def __str__(self):
        return f"Expected Code: {self.expected} got: {self.actual}"


class Codimd:

    def __init__(self, url):
        self.url = url
        self.protocol = None
        self.domain = None
        self.note_id = None

    def parse_url(self):
        # "https?://(?P<domain>\S+)/(?P<id>[a-zA-Z0-9_]*)(\?(both|view|edit))?"
        reg = re.compile(r'(?P<protocol>https?)://(?P<domain>\S+)/(?P<noteid>[a-zA-Z0-9_-]*)(\?(both|view|edit))?(#.*)?')
        match = reg.fullmatch(self.url)

        if match is not None:
            self.note_id = match["noteid"]
            self.domain = match["domain"]
            self.protocol = match["protocol"]
            return True
        else:
            return False

    def get_md(self):
        if self.protocol is not None and self.domain is not None and self.note_id is not None:
            url = f"{self.protocol}://{self.domain}/{self.note_id}/download"
            try:
                data = requests.get(url)
            except ConnectionError:
                return "Connection to server failed!"

            if data.status_code is 200:
                return data.text
            else:
                raise StatusCodeError(200, data.status_code)
        else:
            raise AttributeError("No complete url")

