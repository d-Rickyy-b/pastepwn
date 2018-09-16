# -*- coding: utf-8 -*-
import logging
from queue import Queue
from threading import Event

from actions import DatabaseAction
from analyzers import AlwaysTrueAnalyzer
from core import ScrapingHandler, ActionHandler
from database import MongoDB
from core.pastedispatcher import PasteDispatcher


class PastePwn(object):

    def __init__(self, store_pastes=True, db_ip="127.0.0.1", db_port=27017):
        self.logger = logging.getLogger(__name__)
        self.database = None
        self.paste_queue = Queue()
        self.action_queue = Queue()
        self.__exception_event = Event()

        self.scraping_handler = ScrapingHandler(paste_queue=self.paste_queue,
                                                exception_event=self.__exception_event)
        self.paste_dispatcher = PasteDispatcher(paste_queue=self.paste_queue,
                                                action_queue=self.action_queue,
                                                exception_event=self.__exception_event)
        self.action_handler = ActionHandler(action_queue=self.action_queue,
                                            exception_event=self.__exception_event)

        # TODO more dynamic approach to be able to add different DBMS such as Mongo, sqlite, mysql
        if store_pastes:
            if db_ip is None or db_port is None:
                self.logger.warning("No DB IP/Port specified. Not storing pastes in a database!")
            elif db_ip is not None and db_port is not None:
                self.logger.info("Initalizing database")
                try:
                    self.database = MongoDB(ip=db_ip, port=db_port)
                except Exception as e:
                    self.logger.error("Exception raised while connecting to the database: {0}".format(e))
                    self.__exception_event.set()
                    self.database = None

            if self.database is not None:
                # Save every paste to the database with the AlwaysTrueAnalyzer
                database_action = DatabaseAction(self.database)
                always_true = AlwaysTrueAnalyzer(database_action)
                self.add_analyzer(always_true)

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
