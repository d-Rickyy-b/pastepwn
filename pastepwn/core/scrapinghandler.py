# -*- coding: utf-8 -*-

import logging
from queue import Queue
from threading import Lock, Event

from pastepwn.util import start_thread


class ScrapingHandler(object):
    """Class to handle all the given scrapers to fetch pastes from different sources"""

    def __init__(self, paste_queue=None, exception_event=None):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.__exception_event = exception_event or Event()
        self.paste_queue = paste_queue or Queue()
        self.__lock = Lock()
        self.__threads = []
        self.scrapers = []

    def add_scraper(self, scraper):
        self.scrapers.append(scraper)

    def start(self):
        """Starts scraping pastes from the provided sources"""
        with self.__lock:
            if not self.running:
                # There needs to be at least one scraper
                if len(self.scrapers) == 0:
                    self.logger.warning("No scrapers added! At least one scraper must be added prior to use!")
                    return None

                self.running = True
                # Start all scraper threads
                for scraper in self.scrapers:
                    thread = start_thread(scraper.start, scraper.name, paste_queue=self.paste_queue, exception_event=self.__exception_event)
                    self.__threads.append(thread)

                # Return the update queue so the main thread can insert updates
                return self.paste_queue

    def stop(self):
        with self.__lock:
            if not self.running:
                return

            self.logger.debug("Stopping scrapers...")
            self.running = False
            for scraper in self.scrapers:
                scraper.stop()
            self._join_threads()

    def _join_threads(self):
        """End all threads and join them back into the main thread"""
        for thread in self.__threads:
            self.logger.debug("Joining thread {0}".format(thread.name))
            thread.join()
            self.logger.debug("Thread {0} has ended".format(thread.name))

        self.__threads = []
