# -*- coding: utf-8 -*-
from threading import Event
from time import sleep


class BasicScraper(object):
    name = "BasicScraper"

    def __init__(self, exception_event=None):
        self.running = False
        self._stop_event = Event()
        self._exception_event = exception_event or Event()

    def init_exception_event(self, exception_event):
        self._exception_event = exception_event

    def start(self, paste_queue):
        raise NotImplementedError

    def stop(self):
        if self.running:
            self._stop_event.set()
            while self.running:
                sleep(0.1)
            self._stop_event.clear()
