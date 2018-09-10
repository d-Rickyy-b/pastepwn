# -*- coding: utf-8 -*-

import logging.handlers
import os

from actions import SaveFileAction, LogAction
from analyzers import MailAnalyzer, WordAnalyzer
from pastedispatcher import PasteDispatcher
from scraping import ScrapingHandler
from scraping.pastebin import PastebinScraper

logdir_path = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(logdir_path, "logs", "pastepwn.log")

if not os.path.exists(os.path.join(logdir_path, "logs")):
    os.makedirs(os.path.join(logdir_path, "logs"))

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, 'a', 'utf-8')

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, handlers=[logfile_handler, logging.StreamHandler()])

# Framework code
scraping_handler = ScrapingHandler()
scraping_handler.add_scraper(PastebinScraper())
paste_queue = scraping_handler.start_scraping()

# Define analyzers
mail_analyzer = MailAnalyzer(SaveFileAction(os.path.join(logdir_path, "test.json")))
test_analyzer = WordAnalyzer(LogAction(), "main")

pd = PasteDispatcher(paste_queue, action_queue=None, exception_event=None)
pd.add_analyzer(mail_analyzer)
action_queue = pd.start()


