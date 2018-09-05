# -*- coding: utf-8 -*-


class IPNotRegisteredError(Exception):

    def __init__(self):
        super().__init__("The IP you use for scraping was not whitelisted. Visit https://pastebin.com/doc_scraping_api to get access!")
