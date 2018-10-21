# -*- coding: utf-8 -*-
import logging
from queue import Queue
from threading import Event

from pastepwn.actions import DatabaseAction
from pastepwn.analyzers import AlwaysTrueAnalyzer
from pastepwn.core import ScrapingHandler, ActionHandler
from pastepwn.core.pastedispatcher import PasteDispatcher
from pastepwn.util.request import Request


class PastePwn(object):

    def __init__(self, database=None, proxies=None):
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.paste_queue = Queue()
        self.action_queue = Queue()
        self.__exception_event = Event()
        self.__request = Request(proxies)  # initialize singleton

        # Usage of ipify to get the IP - Uses the X-Forwarded-For Header which might
        # lead to issues with proxies
        ip = self.__request.get("https://api.ipify.org")
        self.logger.info("Your public IP is {0}".format(ip))

        self.scraping_handler = ScrapingHandler(paste_queue=self.paste_queue,
                                                exception_event=self.__exception_event)
        self.paste_dispatcher = PasteDispatcher(paste_queue=self.paste_queue,
                                                action_queue=self.action_queue,
                                                exception_event=self.__exception_event)
        self.action_handler = ActionHandler(action_queue=self.action_queue,
                                            exception_event=self.__exception_event)

        if self.database is not None:
            # Save every paste to the database with the AlwaysTrueAnalyzer
            self.logger.info("Database provided! Storing pastes in there.")
            database_action = DatabaseAction(self.database)
            always_true = AlwaysTrueAnalyzer(database_action)
            self.add_analyzer(always_true)
        else:
            self.logger.info("No database provided!")

    def add_scraper(self, scraper):
        scraper.init_exception_event(self.__exception_event)
        self.scraping_handler.add_scraper(scraper)

    def add_analyzer(self, analyzer):
        self.paste_dispatcher.add_analyzer(analyzer)

    def start(self):
        if not self.__exception_event.is_set():
            self.scraping_handler.start()
            self.paste_dispatcher.start()
            self.action_handler.start()
        else:
            self.logger.error("An exception occured. Aborting the start of PastePwn!")
            exit(1)
