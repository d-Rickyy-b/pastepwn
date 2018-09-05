# -*- coding: utf-8 -*-

import logging
from threading import Event
from queue import Empty


class PasteDispatcher(object):

    logger = logging.getLogger(__name__)

    def __init__(self, paste_queue, analyzers, exception_event=None):
        self.paste_queue = paste_queue
        self.analyzers = analyzers
        self.running = False

        self.__exception_event = exception_event or Event()
        self.__stop_event = Event()

    def start(self, ready=None):
        if self.running:
            self.logger.warning('PasteDispatcher is already running')
            if ready is not None:
                ready.set()
            return

        if self.__exception_event.is_set():
            msg = 'reusing PasteDispatcher after exception event is forbidden'
            self.logger.error(msg)
            raise Exception(msg)

        self.running = True
        self.logger.debug('PasteDispatcher started')

        if ready is not None:
            ready.set()

        while True:
            try:
                # Get paste from queue
                paste = self.paste_queue.get(True, 1)
            except Empty:
                if self.__stop_event.is_set():
                    self.logger.debug('orderly stopping')
                    break
                elif self.__exception_event.is_set():
                    self.logger.critical('stopping due to exception in another thread')
                    break
                continue

            self.logger.debug('Processing Paste: %s' % paste)
            self.process_paste(paste)

        self.running = False
        self.logger.debug('PasteDispatcher thread stopped')

    def process_paste(self, paste):
        for analyzer in self.analyzers:
            if analyzer.match(paste):
                # TODO add to action queue
                # action = analyzer.action
                # action_queue.put(action)
                pass
