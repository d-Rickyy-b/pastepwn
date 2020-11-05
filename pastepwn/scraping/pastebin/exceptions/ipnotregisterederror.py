# -*- coding: utf-8 -*-
import re


class IPNotRegisteredError(Exception):
    """Exception class indicating that your IP is not witelisted on pastebin"""

    def __init__(self, body):
        """
        Initialize the interface.

        Args:
            self: (todo): write your description
            body: (str): write your description
        """
        ip = re.search("YOUR IP: (.*?) DOES NOT HAVE ACCESS", body).group(1)
        super().__init__("The IP you use for scraping ({0}) was not whitelisted. Visit https://pastebin.com/doc_scraping_api to get access!".format(ip))
