# -*- coding: utf-8 -*-

import logging
from queue import Empty, Queue
from threading import Event, Lock
from time import sleep

from pastepwn.util import start_thread, join_threads


class ActionHandler(object):
    """Handler to execute all the actions, if an analyzer matches a paste"""

    def __init__(self, action_queue=None, exception_event=None, stop_event=None):
        self.logger = logging.getLogger(__name__)
        self.action_queue = action_queue or Queue()
        self.__exception_event = exception_event or Event()
        self.__stop_event = stop_event or Event()
        self.__threads = []

        self.running = False
        self.__lock = Lock()

    def start(self, ready=None):
        """
        Starts the actionhandler to execute actions if pastes are matched
        :param ready: Event to check from the outside if the actionhandler has been started
        :return: None
        """
        with self.__lock:
            if not self.running:
                self.running = True

                thread = start_thread(self._start, "ActionHandler", self.__exception_event)
                self.__threads.append(thread)

            if ready is not None:
                ready.set()

    def stop(self):
        """
        Stops the actionhandler
        :return: None
        """
        self.__stop_event.set()
        while self.running:
            sleep(0.1)
        self.__stop_event.clear()

        join_threads(self.__threads)
        self.__threads = []

    def _start(self):
        while self.running:
            try:
                # Get paste from queue
                actions, paste, analyzer = self.action_queue.get(True, 1)
                if actions is None:
                    continue

                for action in actions:
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
