# -*- coding: utf-8 -*-
from threading import Event
from time import sleep


class BasicScraper(object):
    """Abstract class for scraper instances"""
    name = "BasicScraper"

    def __init__(self, exception_event=None):
        self.running = False
        self._stop_event = Event()
        self._exception_event = exception_event or Event()

    def init_exception_event(self, exception_event):
        """Sets an exception event which can be set in order to stop scraping"""
        self._exception_event = exception_event

    def start(self, paste_queue):
        """Starts the scraping process"""
        raise NotImplementedError

    def stop(self):
        """Stops the scraping process"""
        if self.running:
            self._stop_event.set()
            while self.running:
                sleep(0.1)
            self._stop_event.clear()
