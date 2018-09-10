# -*- coding: utf-8 -*-
import json
import logging
import time
from threading import Thread, current_thread

import certifi
import urllib3

from queue import Queue, Empty
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

    def __init__(self, exception_event=None):
        super().__init__(exception_event)
        self.logger = logging.getLogger(__name__)
        self._last_scrape_time = 0
        self.paste_queue = None
        self._tmp_paste_queue = Queue()
        self._known_pastes = []
        self._known_pastes_limit = 1000

    def _init_thread(self, target, name, *args, **kwargs):
        thr = Thread(target=self._thread_wrapper, name=name, args=(target,) + args, kwargs=kwargs)
        thr.start()

    def _thread_wrapper(self, target, *args, **kwargs):
        thr_name = current_thread().name
        self.logger.debug('{0} - started'.format(thr_name))
        try:
            target(*args, **kwargs)
        except Exception:
            self.__exception_event.set()
            self.logger.exception('unhandled exception in %s', thr_name)
            raise
        self.logger.debug('{0} - ended'.format(thr_name))

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
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
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

    def _get_paste_content(self, key):
        endpoint = "api_scrape_item.php"
        api_url = "{0}/{1}?i={2}".format(self.api_base_url, endpoint, key)
        content = ""

        self.logger.debug("Downloading paste {0}".format(key))
        try:
            http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            response = http.request('GET', api_url)
            response_data = response.data.decode("utf-8")

            self._check_error(response_data)

            content = response_data
        except Exception as e:
            self.logger.error(e)

        return content

    def _body_downloader(self):
        """Downloads the body of pastes from pastebin"""
        while self.running:
            try:
                self.logger.info("Queue size: {}".format(self._tmp_paste_queue.qsize()))

                if self._check_stop_event() or self._check_exception_event():
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

                if diff >= 1:
                    continue

                sleep_diff = round(1 - diff, 3)
                self.logger.debug("Sleep time is: {0}".format(sleep_diff))
                time.sleep(sleep_diff)
            except Empty:
                continue

    def start(self, paste_queue):
        """Start the scraping process and download the paste metadata"""
        self.paste_queue = paste_queue
        self.running = True
        self._init_thread(self._body_downloader, "BodyDownloader")

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

                    self.logger.info("Paste is unknown - adding ot to list {}".format(paste.key))
                    self._tmp_paste_queue.put(paste)
                    self._known_pastes.append(paste.key)
                    counter += 1

                    if self._check_stop_event() or self._check_exception_event():
                        break

                self.logger.debug("{0} new pastes fetched!".format(counter))

            # Delete some of the last pastes to not run into memory/performance issues
            if len(self._known_pastes) > 1000:
                self.logger.debug("known_pastes > 1000 - cleaning up!")
                start_index = len(self._known_pastes) - self._known_pastes_limit
                self._known_pastes = self._known_pastes[start_index:]

            if self._check_stop_event() or self._check_exception_event():
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
