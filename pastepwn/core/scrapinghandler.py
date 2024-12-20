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

    def add_scraper(self, scraper, restart_scraping=False):
        """Adds a scraper to the list of scrapers"""
        self.scrapers.append(scraper)

        if self.running and restart_scraping:
            logging.info("Restarting scrapers...")
            self.stop()
            self.start()

    def start(self):
        """Starts scraping pastes from the provided sources"""
        with self.__lock:
            if not self.running:
                # There needs to be at least one scraper
                if not self.scrapers:
                    self.logger.warning("No scrapers added! At least one scraper must be added prior to use!")
                    return None

                self.running = True
                # Start all scraper threads
                for scraper in self.scrapers:
                    thread = start_thread(scraper.start, scraper.name, paste_queue=self.paste_queue, exception_event=self.__exception_event)
                    self.__threads.append(thread)

                # Return the update queue so the main thread can insert updates
                return self.paste_queue

        return None

    def stop(self):
        """Stops scraping pastes"""
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
            self.logger.debug(f"Joining thread {thread.name}")
            thread.join()
            self.logger.debug(f"Thread {thread.name} has ended")

        self.__threads = []
