import logging
from queue import Empty, Queue
from threading import Event, Lock
from time import sleep

from pastepwn.util import join_threads, start_thread


class PasteDispatcher:
    """The PasteDispatcher dispatches the downloaded pastes to the analyzers"""

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

    def add_analyzer(self, analyzer):
        """Adds an analyzer to the list of analyzers"""
        with self.__lock:
            self.analyzers.append(analyzer)

    def start(self, workers=4, ready=None):
        """Starts dispatching the downloaded pastes to the list of analyzers"""
        with self.__lock:
            if not self.running:
                if not self.analyzers:
                    self.logger.warning("No analyzers added! At least one analyzer must be added prior to use!")
                    return None

                self.running = True
                thread = start_thread(self._start_analyzing, "PasteDispatcher", exception_event=self.__exception_event)
                self.__threads.append(thread)

                # Start thread pool with worker threads
                # for i in range(workers):
                #    thread = Thread(target=self._pool_thread, name="analyzer_{0}".format(i))
                #    self.__thread_pool.add(thread)
                #    thread.start()

            if ready is not None:
                ready.set()

            return self.action_queue

    def _start_analyzing(self):
        while self.running:
            try:
                # Get paste from queue
                paste = self.paste_queue.get(True, 1)
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

            # TODO implement thread pool to limit number of parallel executed threads
            # Don't add these threads to the list. Otherwise they will just block the list
            start_thread(self._process_paste, "process_paste", paste=paste, exception_event=self.__exception_event)

    def _process_paste(self, paste):
        self.logger.debug(f"Analyzing Paste: {paste.key}")
        for analyzer in self.analyzers:
            matches = analyzer.match(paste)

            if matches:
                # If the analyzer just returns a boolean, we pass an empty list
                if isinstance(matches, bool):
                    # matches == True, hence we pass an empty list
                    matches = []
                elif not isinstance(matches, list):
                    # when matches is not a bool, we pass the object as list
                    matches = [matches]
                actions = analyzer.actions
                self.action_queue.put((actions, paste, analyzer, matches))

    def stop(self):
        """Stops dispatching pastes to the analyzers"""
        self.__stop_event.set()
        while self.running:
            sleep(0.1)
        self.__stop_event.clear()

        join_threads(self.__threads)
        self.__threads = []
