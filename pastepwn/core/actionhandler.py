# -*- coding: utf-8 -*-

import logging
from queue import Empty, Queue
from threading import Event, Lock

from pastepwn.util import start_thread


class ActionHandler(object):

    def __init__(self, action_queue=None, exception_event=None, stop_event=None):
        self.logger = logging.getLogger(__name__)
        self.action_queue = action_queue or Queue()
        self.__exception_event = exception_event or Event()
        self.__stop_event = stop_event or Event()

        self.running = False
        self.__lock = Lock()

    def start(self, ready=None):
        with self.__lock:
            if not self.running:
                self.running = True

                start_thread(self._start, "ActionHandler", self.__exception_event)

            if ready is not None:
                ready.set()

    def _start(self):
        while self.running:
            try:
                # Get paste from queue
                action, paste, analyzer = self.action_queue.get(True, 1)
                self.logger.debug("Performing action '{0}' on paste '{1}' matched by analyzer '{2}'!".format(action.name, paste.key, analyzer.identifier))
                action.perform(paste, analyzer.identifier)
            except Empty:
                if self.__stop_event.is_set():
                    self.logger.debug("orderly stopping ActionHandler")
                    self.running = False
                    break
                elif self.__exception_event.is_set():
                    self.logger.critical("stopping ActionHandler due to exception in another thread")
                    self.running = False
                    break
