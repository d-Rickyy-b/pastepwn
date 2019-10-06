# -*- coding: utf-8 -*-

import logging.handlers
import os

from pastepwn import PastePwn
from pastepwn.actions import TelegramAction
from pastepwn.analyzers import MailAnalyzer, WordAnalyzer
from pastepwn.database import MongoDB

# Setting up the logging
logdir_path = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(logdir_path, "logs", "pastepwn.log")

if not os.path.exists(os.path.join(logdir_path, "logs")):
    os.makedirs(os.path.join(logdir_path, "logs"))

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, handlers=[logfile_handler, logging.StreamHandler()])

# Framework code
database = MongoDB(ip="192.168.240.128")

pastepwn = PastePwn(database)

# Generic action to send Telegram messages on new matched pastes
telegram_action = TelegramAction(token="token", receiver="-1001348376474")

mail_analyzer = MailAnalyzer(telegram_action)
premium_analyzer = WordAnalyzer(telegram_action, "premium")

pastepwn.add_analyzer(mail_analyzer)
pastepwn.add_analyzer(premium_analyzer)

pastepwn.start()
