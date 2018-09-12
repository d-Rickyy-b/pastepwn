# -*- coding: utf-8 -*-
from pastedispatcher import PasteDispatcher
from scraping import ScrapingHandler
from queue import Queue
from scraping.pastebin import PastebinScraper


class PastePwn(object):

    def __init__(self, mongo_ip=None, mongo_port=None):
        self.paste_queue = Queue()
        self.action_queue = Queue()
        self.scraping_handler = ScrapingHandler(self.paste_queue)
        self.paste_dispatcher = PasteDispatcher(self.paste_queue,
                                                action_queue=self.action_queue,
                                                exception_event=None)

    def add_scraper(self, scraper):
        self.scraping_handler.add_scraper(scraper)

    def add_analyzer(self, analyzer):
        self.paste_dispatcher.add_analyzer(analyzer)

    def start(self):
        self.scraping_handler.start()
        self.paste_dispatcher.start()

