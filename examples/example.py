# -*- coding: utf-8 -*-

import logging.handlers
import os

from actions import TelegramAction
from analyzers import MailAnalyzer, WordAnalyzer
from core import PastePwn
from scraping.pastebin import PastebinScraper

logdir_path = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(logdir_path, "logs", "pastepwn.log")

if not os.path.exists(os.path.join(logdir_path, "logs")):
    os.makedirs(os.path.join(logdir_path, "logs"))

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, 'a', 'utf-8')

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, handlers=[logfile_handler, logging.StreamHandler()])

# Framework code
pastepwn = PastePwn(db_ip="192.168.240.128")
pastepwn.add_scraper(PastebinScraper())

telegram_action = TelegramAction(token="token", receiver="-1001348376474")

mail_analyzer = MailAnalyzer(telegram_action)
premium_analyzer = WordAnalyzer(telegram_action, "premium")

pastepwn.add_analyzer(mail_analyzer)
pastepwn.add_analyzer(premium_analyzer)

pastepwn.start()
