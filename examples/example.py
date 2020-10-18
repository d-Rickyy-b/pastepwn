# -*- coding: utf-8 -*-

import logging.handlers
import pathlib

from pastepwn import PastePwn
from pastepwn.actions import TelegramAction
from pastepwn.analyzers import MailAnalyzer, WordAnalyzer
from pastepwn.database import MongoDB

# Setting up the logging to a file in ./logs/
logdir_path = pathlib.Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("pastepwn.log")

# Creates ./logs/ if it doesn't exist
if not logdir_path.exists():
    logdir_path.mkdir()

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
