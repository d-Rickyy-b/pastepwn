# -*- coding: utf-8 -*-
import json
import logging

import urllib3

from paste import Paste
from scraping import BasicScraper
from scraping.pastebin.exceptions import IPNotRegisteredError, EmptyBodyException


# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.


class PastebinScraper(BasicScraper):
    api_base_url = "https://scrape.pastebin.com"

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def check_error(body):
        """Checks if an error occurred and raises an exception if it did"""
        if body is None:
            raise EmptyBodyException()

        if "DOES NOT HAVE ACCESS" in body:
            raise IPNotRegisteredError()

    def get_recent(self, limit=10):
        endpoint = "api_scraping.php"
        api_url = "{0}/{1}?limit={2}".format(self.api_base_url, endpoint, limit)

        try:
            http = urllib3.PoolManager()
            response = http.request('GET', api_url)
            response_data = response.data.decode("utf-8")

            self.check_error(response_data)

            pastes_dict = json.loads(response_data)
            pastes = []

            for paste in pastes_dict:
                paste_obj = Paste(key=paste.get("key"),
                                  title=paste.get("title"),
                                  user=paste.get("user"),
                                  size=paste.get("size"),
                                  date=paste.get("date"),
                                  expire=paste.get("expire"),
                                  syntax=paste.get("syntax"),
                                  scrape_url=paste.get("scrape_url"),
                                  full_url=paste.get("full_url"))
                pastes.append(paste_obj)

            return pastes
        except Exception as e:
            self.logger.error(e)

    def get_paste(self, key):
        endpoint = "api_scrape_item.php"
        api_url = "{0}/{1}?i={2}".format(self.api_base_url, endpoint, key)
        paste = None

        try:
            http = urllib3.PoolManager()
            response = http.request('GET', api_url)
            response_data = response.data.decode("utf-8")

            self.check_error(response_data)
        except Exception as e:
            self.logger.error(e)

        return paste

    def scrape(self):
        pass
