# -*- coding: utf-8 -*-

import logging
from queue import Empty, Queue
from threading import Event
from threading import Thread, Lock, current_thread


class PasteDispatcher(object):

    def __init__(self, paste_queue, action_queue=None, exception_event=None):
        self.logger = logging.getLogger(__name__)
        self.paste_queue = paste_queue
        self.action_queue = action_queue or Queue()
        self.analyzers = []
        self.running = False

        self.__lock = Lock()
        self.__threads = []
        self.__thread_pool = set()
        self.__exception_event = exception_event or Event()
        self.__stop_event = Event()

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


    def add_analyzer(self, analyzer):
        self.analyzers.append(analyzer)

    def start(self, workers=4, ready=None):
        """Starts dispatching the downloaded pastes to the list of analyzers"""
        with self.__lock:
            if not self.running:
                if len(self.analyzers) == 0:
                    self.logger.warning("No analyzers added! At least one analyzer must be added prior to use!")
                    return None

                self.running = True
                self._init_thread(self._start_analyzing, "PasteDispatcher")

                self.logger.debug("PasteDispatcher started")

            if ready is not None:
                ready.set()

            return self.action_queue

    def _start_analyzing(self):
        while self.running:
            try:
                # Get paste from queue
                paste = self.paste_queue.get(True, 1)

                # TODO implement thread pool to limit number of parallel executed threads
                self._init_thread(self._process_paste, "process_paste", paste=paste)
            except Empty:
                if self.__stop_event.is_set():
                    self.logger.debug("orderly stopping")
                    self.running = False
                    break
                elif self.__exception_event.is_set():
                    self.logger.critical("stopping due to exception in another thread")
                    self.running = False
                    break
                continue

    def _process_paste(self, paste):
        self.logger.debug("Analyzing Paste: {0}".format(paste.key))
        for analyzer in self.analyzers:
            if analyzer.match(paste):
                action = analyzer.action
                self.action_queue.put((action, paste, analyzer))
