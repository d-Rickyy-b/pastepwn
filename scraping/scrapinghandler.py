# -*- coding: utf-8 -*-

import logging
from queue import Queue
from threading import Thread, Lock, current_thread, Event


class ScrapingHandler(object):
    """Class to handle all the given scraping to fetch pastes from different sources"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.__exception_event = Event()
        self.paste_queue = Queue()
        self.__lock = Lock()
        self.__threads = []
        self.scrapers = []

    def _init_thread(self, target, name, *args, **kwargs):
        thr = Thread(target=self._thread_wrapper, name=name, args=(target,) + args, kwargs=kwargs)
        thr.start()
        self.__threads.append(thr)

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

    def add_scraper(self, scraper):
        self.scrapers.append(scraper)

    def start_scraping(self):
        """Starts scraping pastes from the provided sources"""
        with self.__lock:
            if not self.running:
                self.running = True

                # There needs to be at least one scraper
                if len(self.scrapers) == 0:
                    self.logger.warning("No scrapers added!")
                    self.running = False
                    return

                # Start all scraper threads
                for scraper in self.scrapers:
                    self._init_thread(scraper.start, scraper.name, paste_queue=self.paste_queue)

                # Return the update queue so the main thread can insert updates
                return self.paste_queue

    def stop(self):
        with self.__lock:
            if self.running:
                self.logger.debug("Stopping scraping...")
                self.running = False
                self._join_threads()

    def _join_threads(self):
        """End all threads and join them back into the main thread"""
        for thread in self.__threads:
            self.logger.debug("Joining thread {0}".format(thread.name))
            thread.join()
            self.logger.debug("Thread {0} has ended".format(thread.name))

        self.__threads = []

# TODO implement idle for SIGINT, SIGTERM, SIGKILL
