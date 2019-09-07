# -*- coding: utf-8 -*-
import json
import logging
import re
import time
from queue import Queue, Empty

from pastepwn.core import Paste
from pastepwn.scraping import BasicScraper
from pastepwn.scraping.pastebin.exceptions import IPNotRegisteredError, PasteDeletedException, PasteNotReadyException, PasteEmptyException
from pastepwn.util import Request, start_thread


# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.


class PastebinScraper(BasicScraper):
    """Scraper class for pastebin"""
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

    def _check_error(self, body, key=None):
        """Checks if an error occurred and raises an exception if it did"""
        pattern = r"YOUR IP: \d{1,3}.\d{1,3}.\d{1,3}.\d{1,3} DOES NOT HAVE ACCESS\.\s+VISIT: https:\/\/pastebin\.com\/doc_scraping_api TO GET ACCESS!"

        if 107 >= len(body) >= 99 and re.match(pattern, body):
            self._exception_event.set()
            raise IPNotRegisteredError(body)

        if body is None or body == "":
            raise PasteEmptyException("The paste '{0}' or its body was set to None!".format(key))
        if body == "File is not ready for scraping yet. Try again in 1 minute.":
            # The pastebin API was not ready yet to deliver this paste -
            # We raise an exception to re-download it again after some time has passed
            raise PasteNotReadyException("The paste '{0}' could not be fetched yet!".format(key))
        elif body == "Error, we cannot find this paste.":
            # The paste has been deleted before we could download it.
            # We raise an exception to delete the paste from the queue
            raise PasteDeletedException("The paste '{0}' has been deleted!".format(key))

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

        self.logger.debug("Downloading paste {0}".format(key))
        try:
            response_data = r.get(api_url)
        except Exception as e:
            self.logger.error(e)
            raise e

        self._check_error(response_data, key)

        return response_data

    def _body_downloader(self):
        """Downloads the body of pastes from pastebin, which have been put into the queue"""
        while self.running:
            try:
                if self._tmp_paste_queue.qsize() > 0:
                    self.logger.debug("Queue size: {}".format(self._tmp_paste_queue.qsize()))

                if self._stop_event.is_set() or self._exception_event.is_set():
                    self.logger.debug("Stop or exception event is set!")
                    self.running = False
                    break

                paste = self._tmp_paste_queue.get(True, 1)

                # if paste is not known, download the body and put it on the queue and into the list
                last_body_download_time = round(time.time(), 2)

                try:
                    body = self._get_paste_content(paste.key)
                except PasteNotReadyException:
                    self.logger.debug("Paste '{0}' is not ready for downloading yet. Enqueuing it again.".format(paste.key))
                    # Make sure to wait a certain time. If only one element in the queue, this can lead to loops
                    self._rate_limit_sleep(last_body_download_time)
                    self._tmp_paste_queue.put(paste)
                    continue
                except PasteDeletedException:
                    # We don't add a sleep here, because this can't lead to loops
                    self.logger.info("Paste '{0}' has been deleted before we could download it! Skipping paste.".format(paste.key))
                    continue
                except PasteEmptyException:
                    self.logger.info("Paste '{0}' is set to None! Skipping paste.".format(paste.key))
                    continue
                except Exception as e:
                    self.logger.error("An exception occurred while downloading the paste '{0}'. Skipping this paste! Exception is: {1}".format(paste.key, e))
                    continue

                paste.set_body(body)
                self.paste_queue.put(paste)

                self._rate_limit_sleep(last_body_download_time)
            except Empty:
                continue

    def _rate_limit_sleep(self, last_body_download_time):
        """
        Sleeps a certain amount of seconds to prevent hitting API rate limits
        :param last_body_download_time: The time when the last paste was downloaded
        :return:
        """
        current_time = round(time.time(), 2)
        diff = round(current_time - last_body_download_time, 2)

        if diff >= self._api_hit_rate:
            return

        sleep_diff = round(self._api_hit_rate - diff, 3)
        self.logger.debug("Sleep time is: {0}".format(sleep_diff))
        time.sleep(sleep_diff)

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

            while self.running:
                current_time = int(time.time())
                diff = current_time - self._last_scrape_time

                if diff > 60:
                    break

                # if the last scraping happened less than 60 seconds ago,
                # wait 2 seconds and check again
                time.sleep(2)
