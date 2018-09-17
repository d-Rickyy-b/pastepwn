# -*- coding: utf-8 -*-

import logging
from queue import Empty, Queue
from threading import Event
from threading import Thread, Lock, current_thread


class ActionHandler(object):

    def __init__(self, action_queue=None, exception_event=None, stop_event=None):
        self.logger = logging.getLogger(__name__)
        self.action_queue = action_queue or Queue()
        self.__exception_event = exception_event or Event()
        self.__stop_event = stop_event or Event()

        self.running = False
        self.__lock = Lock()

    def _init_thread(self, target, name, *args, **kwargs):
        thr = Thread(target=self._thread_wrapper, name=name, args=(target,) + args, kwargs=kwargs)
        thr.start()

    def _thread_wrapper(self, target, *args, **kwargs):
        thr_name = current_thread().name
        self.logger.debug('{0} - started'.format(thr_name))
        try:
            target(*args, **kwargs)
        except Exception:
            self.logger.exception('unhandled exception in %s', thr_name)
            raise
        self.logger.debug('{0} - ended'.format(thr_name))

    def start(self, ready=None):
        with self.__lock:
            if not self.running:
                self.running = True

                self._init_thread(self._start, "ActionHandler")

            if ready is not None:
                ready.set()

    def _start(self):
        while self.running:
            try:
                # Get paste from queue
                action, paste, analyzer = self.action_queue.get(True, 1)
                self.logger.debug("Performing action '{0}' on paste '{1}' matched by analyzer '{2}'!".format(action.name, paste.key, analyzer.identifier))
                action.perform(paste, analyzer.name)
            except Empty:
                if self.__stop_event.is_set():
                    self.logger.debug("orderly stopping ActionHandler")
                    self.running = False
                    break
                elif self.__exception_event.is_set():
                    self.logger.critical("stopping ActionHandler due to exception in another thread")
                    self.running = False
                    break
                continue
