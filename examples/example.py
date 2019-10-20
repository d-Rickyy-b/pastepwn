# -*- coding: utf-8 -*-

import logging.handlers
import pathlib

from pastepwn import PastePwn
from pastepwn.actions import TelegramAction
from pastepwn.analyzers import MailAnalyzer, WordAnalyzer
from pastepwn.database import MongoDB

# Setup logging to a file in ./logs/
logdir_path = pathlib.Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("pastepwn.log")

# Creates ./logs/ if it doesen't exist
if not logdir_path.exists():
    logdir_path.mkdir()

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, handlers=[logfile_handler, logging.StreamHandler()])

# Create a database connection and setup pastepwn
database = MongoDB(ip="192.168.240.128")
pastepwn = PastePwn(database)

# Generic action to send Telegram messages on new matched pastes
telegram_action = TelegramAction(token="token", receiver="-1001348376474")

# Associate mail and word analyzers with the telegram action and add then to pastpwn
mail_analyzer = MailAnalyzer(telegram_action)
premium_analyzer = WordAnalyzer(telegram_action, "premium")

pastepwn.add_analyzer(mail_analyzer)
pastepwn.add_analyzer(premium_analyzer)

# Start pastepwn and log that we are doing that
logger.debug("Starting pastepwn")
pastepwn.start()
