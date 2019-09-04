# -*- coding: utf-8 -*-
import logging
from queue import Queue
from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Event
from time import sleep

from pastepwn.actions import DatabaseAction
from pastepwn.analyzers import AlwaysTrueAnalyzer
from pastepwn.core import ScrapingHandler, ActionHandler
from pastepwn.core.pastedispatcher import PasteDispatcher
from pastepwn.util.request import Request


class PastePwn(object):
    """Represents an instance of the pastepwn core module"""

    def __init__(self, database=None, proxies=None, store_all_pastes=True):
        """
        Basic PastePwn object handling the connection to pastebin and all the analyzers and actions
        :param database: Database object extending AbstractDB
        :param proxies: Dict of proxies as defined in the requests documentation
        :param store_all_pastes: Bool to decide if all pastes should be stored into the db
        """
        self.logger = logging.getLogger(__name__)
        self.is_idle = False
        self.database = database
        self.paste_queue = Queue()
        self.action_queue = Queue()
        self.error_handlers = list()
        self.__exception_event = Event()
        self.__request = Request(proxies)  # initialize singleton

        # Usage of ipify to get the IP - Uses the X-Forwarded-For Header which might
        # lead to issues with proxies
        try:
            ip = self.__request.get("https://api.ipify.org")
            self.logger.info("Your public IP is {0}".format(ip))
        except Exception as e:
            self.logger.warning("Could not fetch public IP via ipify: {0}".format(e))

        self.scraping_handler = ScrapingHandler(paste_queue=self.paste_queue,
                                                exception_event=self.__exception_event)
        self.paste_dispatcher = PasteDispatcher(paste_queue=self.paste_queue,
                                                action_queue=self.action_queue,
                                                exception_event=self.__exception_event)
        self.action_handler = ActionHandler(action_queue=self.action_queue,
                                            exception_event=self.__exception_event)

        if self.database is not None and store_all_pastes:
            # Save every paste to the database with the AlwaysTrueAnalyzer
            self.logger.info("Database provided! Storing pastes in there.")
            database_action = DatabaseAction(self.database)
            always_true = AlwaysTrueAnalyzer(database_action)
            self.add_analyzer(always_true)
        elif store_all_pastes:
            self.logger.info("No database provided!")
        else:
            self.logger.info("Not storing all pastes!")

    def add_scraper(self, scraper, restart_scraping=False):
        """
        Adds a scraper to the list of scrapers. Scraping handler must be restarted for this to take effect.
        :param scraper: Instance of a BasicScraper
        :param restart_scraping: Indicates if the scraping handler should be restarted. Not setting this option results in your scraper not being started.
        :return: None
         """
        scraper.init_exception_event(self.__exception_event)
        self.scraping_handler.add_scraper(scraper, restart_scraping)

    def add_analyzer(self, analyzer):
        """
        Adds a new analyzer to the list of analyzers
        :param analyzer: Instance of an BasicAnalyzer
        :return: None
        """

        self.paste_dispatcher.add_analyzer(analyzer)

    def add_error_handler(self, error_handler):
        """
        Adds an error handler which will be called when an error happens
        :param error_handler: Callable to be called when an error happens
        :return: None
        """
        if not callable(error_handler):
            self.logger.error("The error handler you passed is not a function!")
            return

        self.error_handlers.append(error_handler)

    def start(self):
        """Starts the pastepwn instance"""
        if self.__exception_event.is_set():
            self.logger.error("An exception occured. Aborting the start of PastePwn!")
            exit(1)

        self.scraping_handler.start()
        self.paste_dispatcher.start()
        self.action_handler.start()

    def stop(self):
        """Stops the pastepwn instance"""
        self.scraping_handler.stop()
        self.paste_dispatcher.stop()
        self.action_handler.stop()
        self.is_idle = False

    def signal_handler(self, signum, frame):
        """Handler method to handle signals"""
        self.is_idle = False
        self.logger.info("Received signal {}, stopping...".format(signum))
        self.stop()

    def idle(self, stop_signals=(SIGINT, SIGTERM, SIGABRT)):
        """
        Blocks until one of the signals are received and stops the updater.
        Thanks to the python-telegram-bot developers - https://github.com/python-telegram-bot/python-telegram-bot/blob/2cde878d1e5e0bb552aaf41d5ab5df695ec4addb/telegram/ext/updater.py#L514-L529
        :param stop_signals: The signals to which the code reacts to
        """
        self.is_idle = True
        self.logger.info("In Idle!")

        for sig in stop_signals:
            signal(sig, self.signal_handler)

        while self.is_idle:
            if self.__exception_event.is_set():
                self.logger.warning("An exception occurred. Calling exception handlers and going down!")
                for handler in self.error_handlers:
                    # call the error handlers in case of an exception
                    handler()
                self.is_idle = False
                self.stop()
                return

            sleep(1)
