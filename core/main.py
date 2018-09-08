# -*- coding: utf-8 -*-

import logging.handlers
import os
import time

from scraping import ScrapingHandler
from scraping.pastebin import PastebinScraper

logdir_path = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(logdir_path, "logs", "pastepwn.log")

if not os.path.exists(os.path.join(logdir_path, "logs")):
    os.makedirs(os.path.join(logdir_path, "logs"))

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, 'a', 'utf-8')


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, handlers=[logfile_handler, logging.StreamHandler()])

# Use long polling for fetching the pastes

#

