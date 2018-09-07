# -*- coding: utf-8 -*-
import json
import logging
import time

import urllib3

from paste import Paste
from scraping import BasicScraper
from scraping.pastebin.exceptions import IPNotRegisteredError, EmptyBodyException


# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.


class PastebinScraper(BasicScraper):
    name = "PastebinScraper"
    api_base_url = "https://scrape.pastebin.com"

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._last_scrape_time = 0
        self.paste_queue = None
        self._known_pastes = []
        self._known_pastes_limit = 1000

    @staticmethod
    def _check_error(body):
        """Checks if an error occurred and raises an exception if it did"""
        if body is None:
            raise EmptyBodyException()

        if "DOES NOT HAVE ACCESS" in body:
            raise IPNotRegisteredError()

    def _get_recent(self, limit=10):
        endpoint = "api_scraping.php"
        api_url = "{0}/{1}?limit={2}".format(self.api_base_url, endpoint, limit)

        try:
            http = urllib3.PoolManager()
            response = http.request('GET', api_url)
            response_data = response.data.decode("utf-8")

            self._check_error(response_data)

            pastes_dict = json.loads(response_data)
            pastes = []

            # Loop through the response and create objects by the data
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

    def _get_paste(self, key):
        endpoint = "api_scrape_item.php"
        api_url = "{0}/{1}?i={2}".format(self.api_base_url, endpoint, key)
        paste = None

        self.logger.debug("Downloading paste")

        try:
            http = urllib3.PoolManager()
            response = http.request('GET', api_url)
            response_data = response.data.decode("utf-8")

            self._check_error(response_data)
        except Exception as e:
            self.logger.error(e)

        return paste

    def start(self, paste_queue):
        self.paste_queue = paste_queue

        while True:
            self._last_scrape_time = int(time.time())
            pastes = self._get_recent(limit=100)
            for paste in pastes:
                # check if paste is in list of known pastes
                if paste.key in self._known_pastes:
                    # Do nothing, if it's already known
                    continue

                # if paste is not known, download the body and put it on the queue and into the list
                # TODO this request must be limited! (1 per second)
                # Maybe move into own thread
                paste.set_body(self._get_paste(paste.key))

                self.paste_queue.put(paste)
                self._known_pastes.append(paste.key)

            # Delete some of the last pastes to not run into memory/performance issues
            if len(self._known_pastes) > 1000:
                start_index = len(self._known_pastes)-self._known_pastes_limit
                self._known_pastes = self._known_pastes[start_index:]

            # check if time since last
            current_time = int(time.time())
            diff = current_time - self._last_scrape_time

            # if the last scraping happened less than 60 seconds ago,
            # wait until the 60 seconds passed
            if diff < 60:
                sleep_time = 60 - diff
                time.sleep(sleep_time)
