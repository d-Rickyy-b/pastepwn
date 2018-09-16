# -*- coding: utf-8 -*-
from threading import Event
from time import sleep


class BasicScraper(object):
    name = "BasicScraper"

    def __init__(self, exception_event=None):
        self.running = False
        self.__stop_event = Event()
        self.__exception_event = exception_event or Event()

    def _check_stop_event(self):
        return self.__stop_event.is_set()

    def _check_exception_event(self):
        return self.__exception_event.is_set()

    def _set_exception_even(self):
        self.__exception_event.set()

    def init_exception_event(self, exception_event):
        self.__exception_event = exception_event

    def start(self, paste_queue):
        raise NotImplementedError

    def stop(self):
        if self.running:
            self.__stop_event.set()
            while self.running:
                sleep(0.1)
            self.__stop_event.clear()
