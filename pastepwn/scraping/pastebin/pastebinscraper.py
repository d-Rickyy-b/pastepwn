# -*- coding: utf-8 -*-
import json
import logging
import time
from queue import Queue, Empty

from pastepwn.core import Paste
from pastepwn.scraping import BasicScraper
from pastepwn.scraping.pastebin.exceptions import IPNotRegisteredError, EmptyBodyException
from pastepwn.util import Request, start_thread


# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.


class PastebinScraper(BasicScraper):
    name = "PastebinScraper"
    api_base_url = "https://scrape.pastebin.com"

    def __init__(self, paste_queue=None, exception_event=None, api_hit_rate=None):
        super().__init__(exception_event)
        self.logger = logging.getLogger(__name__)
        self._last_scrape_time = 0
        self.paste_queue = paste_queue or Queue()
        self._tmp_paste_queue = Queue()

        self._known_pastes = []
        self._known_pastes_limit = 1000

        # The hit rate describes the interval between two requests in seconds
        self._api_hit_rate = api_hit_rate or 1

    def _check_error(self, body):
        """Checks if an error occurred and raises an exception if it did"""
        if body is None:
            raise EmptyBodyException()

        if "DOES NOT HAVE ACCESS" in body:
            self._exception_event.set()
            raise IPNotRegisteredError(body)

    def _get_recent(self, limit=100):
        """Downloads a list of the most recent pastes - the amount is limited by the <limit> parameter"""
        r = Request()
        endpoint = "api_scraping.php"
        api_url = "{0}/{1}?limit={2}".format(self.api_base_url, endpoint, limit)

        try:
            response_data = r.get(api_url)

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
            return None

    def _get_paste_content(self, key):
        """Downloads the content of a certain paste"""
        r = Request()
        endpoint = "api_scrape_item.php"
        api_url = "{0}/{1}?i={2}".format(self.api_base_url, endpoint, key)
        content = ""

        self.logger.debug("Downloading paste {0}".format(key))
        try:
            response_data = r.get(api_url)

            self._check_error(response_data)

            content = response_data
        except Exception as e:
            self.logger.error(e)

        return content

    def _body_downloader(self):
        """Downloads the body of pastes from pastebin, which have been put into the queue"""
        while self.running:
            try:
                if self._tmp_paste_queue.qsize() > 0:
                    self.logger.debug("Queue size: {}".format(self._tmp_paste_queue.qsize()))

                if self._stop_event.is_set() or self._exception_event.is_set():
                    self.running = False
                    break

                paste = self._tmp_paste_queue.get(True, 1)

                # if paste is not known, download the body and put it on the queue and into the list
                last_body_download_time = round(time.time(), 2)
                body = self._get_paste_content(paste.key)

                paste.set_body(body)
                self.paste_queue.put(paste)

                current_time = round(time.time(), 2)
                diff = round(current_time - last_body_download_time, 2)

                if diff >= self._api_hit_rate:
                    continue

                sleep_diff = round(self._api_hit_rate - diff, 3)
                self.logger.debug("Sleep time is: {0}".format(sleep_diff))
                time.sleep(sleep_diff)
            except Empty:
                continue

    def start(self, paste_queue):
        """Start the scraping process and download the paste metadata"""
        self.paste_queue = paste_queue
        self.running = True
        start_thread(self._body_downloader, "BodyDownloader", self._exception_event)

        while self.running:
            self._last_scrape_time = int(time.time())
            pastes = self._get_recent(limit=100)
            counter = 0

            if pastes is not None:
                for paste in pastes:
                    # check if paste is in list of known pastes
                    if paste.key in self._known_pastes:
                        # Do nothing, if it's already known
                        continue

                    self.logger.debug("Paste is unknown - adding ot to list {}".format(paste.key))
                    self._tmp_paste_queue.put(paste)
                    self._known_pastes.append(paste.key)
                    counter += 1

                    if self._stop_event.is_set() or self._exception_event.is_set():
                        self.running = False
                        break

                self.logger.debug("{0} new pastes fetched!".format(counter))

            # Delete some of the last pastes to not run into memory/performance issues
            if len(self._known_pastes) > 1000:
                self.logger.debug("known_pastes > 1000 - cleaning up!")
                start_index = len(self._known_pastes) - self._known_pastes_limit
                self._known_pastes = self._known_pastes[start_index:]

            if self._stop_event.is_set() or self._exception_event.is_set():
                self.logger.debug('stopping {0}'.format(self.name))
                self.running = False
                break

            # check if time since last
            current_time = int(time.time())
            diff = current_time - self._last_scrape_time

            # if the last scraping happened less than 60 seconds ago,
            # wait until the 60 seconds passed
            if diff < 60:
                sleep_time = 60 - diff
                time.sleep(sleep_time)
