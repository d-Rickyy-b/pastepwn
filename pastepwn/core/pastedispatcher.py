import logging
from concurrent.futures import ThreadPoolExecutor
from queue import Empty, Queue
from threading import Event, Lock
from time import sleep

from pastepwn.util import join_threads, start_thread


class PasteDispatcher:
    """The PasteDispatcher dispatches the downloaded pastes to the analyzers"""

    def __init__(self, paste_queue, action_queue=None, exception_event=None, max_workers=4):
        self.logger = logging.getLogger(__name__)
        self.paste_queue = paste_queue
        self.action_queue = action_queue or Queue()
        self.analyzers = []
        self.running = False
        self.max_workers = max_workers

        self.__lock = Lock()
        self.__threads = []
        self.__thread_pool = None
        self.__exception_event = exception_event or Event()
        self.__stop_event = Event()

    def add_analyzer(self, analyzer):
        """Adds an analyzer to the list of analyzers"""
        with self.__lock:
            self.analyzers.append(analyzer)

    def start(self, workers=None, ready=None):
        """Starts dispatching the downloaded pastes to the list of analyzers"""
        with self.__lock:
            if not self.running:
                if not self.analyzers:
                    self.logger.warning("No analyzers added! At least one analyzer must be added prior to use!")
                    return None

                # Use workers parameter if provided, otherwise use max_workers from constructor
                if workers is not None:
                    self.max_workers = workers

                self.running = True
                thread = start_thread(self._start_analyzing, "PasteDispatcher", exception_event=self.__exception_event)
                self.__threads.append(thread)

            if ready is not None:
                ready.set()

            return self.action_queue

    def _start_analyzing(self):
        """Main processing loop that uses thread pool for concurrent paste processing"""
        with ThreadPoolExecutor(max_workers=self.max_workers, thread_name_prefix="PasteProcessor") as executor:
            self.__thread_pool = executor
            self.logger.info(f"Started thread pool with {self.max_workers} workers")
            
            # Track submitted futures for proper cleanup
            futures = set()
            
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

                # Submit paste processing to thread pool
                future = executor.submit(self._process_paste, paste)
                futures.add(future)
                
                # Clean up completed futures to prevent memory leaks
                done_futures = {f for f in futures if f.done()}
                futures -= done_futures
                
                # Check for exceptions in completed futures
                for future in done_futures:
                    try:
                        future.result()  # This will raise any exception that occurred
                    except Exception:
                        self.logger.exception("Exception in paste processing thread")
                        self.__exception_event.set()
                        self.running = False
                        break

            # Wait for remaining futures to complete
            self.logger.debug("Waiting for remaining paste processing tasks to complete")
            for future in futures:
                try:
                    future.result()
                except Exception:
                    self.logger.exception("Exception in paste processing thread during shutdown")

    def _process_paste(self, paste):
        """Process a single paste through all analyzers"""
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

        # Shutdown thread pool if it exists
        if self.__thread_pool is not None:
            self.logger.debug("Shutting down thread pool")
            self.__thread_pool.shutdown(wait=True)
            self.__thread_pool = None

        join_threads(self.__threads)
        self.__threads = []
