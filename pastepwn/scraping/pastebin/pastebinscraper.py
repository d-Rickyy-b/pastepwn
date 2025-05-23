import json
import logging
import re
import time
from queue import Empty, Queue

from pastepwn.core import Paste
from pastepwn.scraping import BasicScraper
from pastepwn.scraping.pastebin.exceptions import IPNotRegisteredError, PasteDeletedException, PasteEmptyException, PasteNotReadyException
from pastepwn.util import Request, start_thread

# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.


class PastebinScraper(BasicScraper):
    """Scraper class for pastebin"""

    name = "PastebinScraper"
    api_base_url = "https://scrape.pastebin.com"
    pastebin_error_pattern = re.compile(
        r"YOUR IP: ((\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})|((([0-9A-Fa-f]{1,4}:){7})([0-9A-Fa-f]{1,4})|(([0-9A-Fa-f]{1,4}:){1,6}:)(([0-9A-Fa-f]{1,4}:){0,4})([0-9A-Fa-f]{1,4}))) DOES NOT HAVE ACCESS"
    )

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
        match = self.pastebin_error_pattern.search(body)
        if match:
            self._exception_event.set()
            ip_address = match.group(1)
            raise IPNotRegisteredError(ip_address)

        if body is None or body == "":
            msg = f"The paste '{key}' or its body was set to None!"
            raise PasteEmptyException(msg)
        if body == "File is not ready for scraping yet. Try again in 1 minute.":
            # The pastebin API was not ready yet to deliver this paste -
            # We raise an exception to re-download it again after some time has passed
            msg = f"The paste '{key}' could not be fetched yet!"
            raise PasteNotReadyException(msg)
        if body == "Error, we cannot find this paste.":
            # The paste has been deleted before we could download it.
            # We raise an exception to delete the paste from the queue
            msg = f"The paste '{key}' has been deleted!"
            raise PasteDeletedException(msg)

    def _get_recent(self, limit=100):
        """Downloads a list of the most recent pastes - the amount is limited by the <limit> parameter"""
        r = Request()
        endpoint = "api_scraping.php"
        api_url = f"{self.api_base_url}/{endpoint}?limit={limit}"

        try:
            response_data = r.get(api_url)

            self._check_error(response_data)

            pastes_dict = json.loads(response_data)
            pastes = []

            # Loop through the response and create objects by the data
            for paste in pastes_dict:
                paste_obj = Paste(
                    key=paste.get("key"),
                    title=paste.get("title"),
                    user=paste.get("user"),
                    size=paste.get("size"),
                    date=paste.get("date"),
                    expire=paste.get("expire"),
                    syntax=paste.get("syntax"),
                    scrape_url=paste.get("scrape_url"),
                    full_url=paste.get("full_url"),
                )
                pastes.append(paste_obj)
        except Exception:
            self.logger.exception("An exception occurred while downloading the recent pastes!")
            return None
        else:
            return pastes

    def _get_paste_content(self, key):
        """Downloads the content of a certain paste"""
        r = Request()
        endpoint = "api_scrape_item.php"
        api_url = f"{self.api_base_url}/{endpoint}?i={key}"

        self.logger.debug(f"Downloading paste {key}")
        try:
            response_data = r.get(api_url)
        except Exception:
            self.logger.exception("An exception occurred while downloading the paste content!")
            raise

        self._check_error(response_data, key)

        return response_data

    def _body_downloader(self):
        """Downloads the body of pastes from pastebin, which have been put into the queue"""
        while self.running:
            # Print current approx. size of paste queue
            if self._tmp_paste_queue.qsize() > 0:
                self.logger.debug(f"Queue size: {self._tmp_paste_queue.qsize()}")

            # Check if the stop event or exception events are set
            if self._stop_event.is_set() or self._exception_event.is_set():
                self.logger.debug("Stop or exception event is set!")
                self.running = False
                break

            try:
                paste = self._tmp_paste_queue.get(True, 1)
            except Empty:
                continue

            last_body_download_time = round(time.time(), 2)

            try:
                body = self._get_paste_content(paste.key)
            except PasteNotReadyException:
                self.logger.debug("Paste '%s' is not ready for downloading yet. Enqueuing it again.", paste.key)
                # Make sure to wait a certain time. If only one element in the queue, this can lead to loops
                self._rate_limit_sleep(last_body_download_time)
                self._tmp_paste_queue.put(paste)
                continue
            except PasteDeletedException:
                # We don't add a sleep here, because this can't lead to loops
                self.logger.info("Paste '%s' has been deleted before we could download it! Skipping paste.", paste.key)
                continue
            except PasteEmptyException:
                self.logger.info("Paste '%s' is set to None! Skipping paste.", paste.key)
                continue
            except Exception:
                self.logger.exception("An exception occurred while downloading the paste '%s'. Skipping this paste!", paste.key)
                continue

            paste.set_body(body)
            self.paste_queue.put(paste)

            self._rate_limit_sleep(last_body_download_time)

    def _rate_limit_sleep(self, last_body_download_time):
        """Sleeps a certain amount of seconds to prevent hitting API rate limits
        :param last_body_download_time: The time when the last paste was downloaded
        :return:
        """
        current_time = round(time.time(), 2)
        diff = round(current_time - last_body_download_time, 2)

        if diff >= self._api_hit_rate:
            return

        sleep_diff = round(self._api_hit_rate - diff, 3)
        self.logger.debug("Sleep time is: %s", sleep_diff)
        time.sleep(sleep_diff)

    def start(self, paste_queue):
        """Start the scraping process and download the paste metadata"""
        self.paste_queue = paste_queue
        self.running = True
        known_pastes_treshold = 1000
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

                    self.logger.debug("Paste is unknown - adding ot to list %s", paste.key)
                    self._tmp_paste_queue.put(paste)
                    self._known_pastes.append(paste.key)
                    counter += 1

                    if self._stop_event.is_set() or self._exception_event.is_set():
                        self.running = False
                        break

                self.logger.debug(f"{counter} new pastes fetched!")

            # Delete some of the last pastes to not run into memory/performance issues
            if len(self._known_pastes) > known_pastes_treshold:
                self.logger.debug("known_pastes > %s - cleaning up!", known_pastes_treshold)
                start_index = len(self._known_pastes) - self._known_pastes_limit
                self._known_pastes = self._known_pastes[start_index:]

            if self._stop_event.is_set() or self._exception_event.is_set():
                self.logger.debug("stopping %s", self.name)
                self.running = False
                break

            while self.running:
                current_time = int(time.time())
                diff = current_time - self._last_scrape_time

                minute_in_seconds = 60
                if diff > minute_in_seconds:
                    break

                # if the last scraping happened less than 60 seconds ago,
                # wait 2 seconds and check again
                time.sleep(2)
