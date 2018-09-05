# -*- coding: utf-8 -*-

import logging
from queue import Queue
from threading import Thread, Lock, current_thread, Event


class ScrapeHandler(object):
    """Class to handle all the given scraping to fetch pastes from different sources"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        self.__exception_event = Event()
        self.paste_queue = Queue()
        self.__lock = Lock()
        self.__threads = []

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

    def start_scraping(self):
        """Starts scraping pastes from the provided sources"""
        with self.__lock:
            if not self.running:
                self.running = True

                # Create & start threads
                dispatcher_ready = Event()
                self._init_thread(self._start_scraping, "updater")

                dispatcher_ready.wait()

                # Return the update queue so the main thread can insert updates
                return self.paste_queue

    def _start_scraping(self):
        while self.running:
            # for scraper in scrapers
            # get pastes
            # put them in the queue
            # return True
            pass

# TODO idle
