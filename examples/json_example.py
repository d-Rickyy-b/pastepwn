# -*- coding: utf-8 -*-

import logging.handlers
import pathlib

from pastepwn import PastePwn
from pastepwn.actions import SaveJSONAction
from pastepwn.analyzers import GoogleApiKeyAnalyzer

# Setting up the logging to a file in ./logs/
logdir_path = pathlib.Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("pastepwn.log")

# Creates ./logs/ if it doesn't exist
if not logdir_path.exists():
    logdir_path.mkdir()

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, handlers=[logfile_handler, logging.StreamHandler()])

# A database can be provided to store pastes. This example does not implement a database.
pastepwn = PastePwn()

# PastePWN has 3 components: Scraper, Analyzer, Action.
# This example implements the default Scraper, Google API Key Analyzer, and JSON File Save Action.
# Generic Action to save Pastes to JSON File.
json_path = "./json_pastes"
save_json_action = SaveJSONAction(json_path)

# Google API Key Analyzer with save JSON action.
google_api_key_analyzer = GoogleApiKeyAnalyzer(save_json_action)

# Add the analyzer to the pastepwn instance.
pastepwn.add_analyzer(google_api_key_analyzer)

# Start scraping/saving.
pastepwn.start()
