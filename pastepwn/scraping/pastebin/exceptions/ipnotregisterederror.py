# -*- coding: utf-8 -*-
import re


class IPNotRegisteredError(Exception):

    def __init__(self, body):
        ip = re.search("YOUR IP: (.*?) DOES NOT HAVE ACCESS", body).group(1)
        super().__init__("The IP you use for scraping ({0}) was not whitelisted. Visit https://pastebin.com/doc_scraping_api to get access!".format(ip))
