# -*- coding: utf-8 -*-
import logging
from queue import Queue

from database import Database
from pastedispatcher import PasteDispatcher
from scraping import ScrapingHandler


class PastePwn(object):

    def __init__(self, mongo_ip=None, mongo_port=None):
        self.logger = logging.getLogger(__name__)
        self.paste_queue = Queue()
        self.action_queue = Queue()
        self.scraping_handler = ScrapingHandler(self.paste_queue)
        self.paste_dispatcher = PasteDispatcher(self.paste_queue,
                                                action_queue=self.action_queue,
                                                exception_event=None)

        if mongo_ip is None or mongo_port is None:
            self.logger.warning("No MongoDB IP/Port specified. Not storing pastes in a database!")
            self.database = None
        elif mongo_ip is not None and mongo_port is not None:
            try:
                self.database = Database(ip=mongo_ip, port=mongo_port)
            except Exception as e:
                self.logger.error("Exception raised while connecting to the database: {0}".format(e))
                self.database = None

        # TODO add database action if database is not None

    def add_scraper(self, scraper):
        self.scraping_handler.add_scraper(scraper)

    def add_analyzer(self, analyzer):
        self.paste_dispatcher.add_analyzer(analyzer)

    def start(self):
        self.scraping_handler.start()
        self.paste_dispatcher.start()

