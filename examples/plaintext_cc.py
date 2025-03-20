from __future__ import annotations

import logging.handlers
import typing
from pathlib import Path

from pastepwn import PastePwn
from pastepwn.actions import BasicAction
from pastepwn.analyzers import CreditCardAnalyzer

if typing.TYPE_CHECKING:
    import re

    from pastepwn.core import Paste


# Setup logging
logdir_path = Path(__file__).parent.joinpath("logs").absolute()
logfile_path = logdir_path.joinpath("pastepwn.log")

if not logdir_path.exists():
    logdir_path.mkdir()

logfile_handler = logging.handlers.WatchedFileHandler(logfile_path, "a", "utf-8")

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO, handlers=[logfile_handler, logging.StreamHandler()])


# Subclass BasicAction to append matches to file
class AppendCCMatchFileAction(BasicAction):
    def __init__(self, path: Path):
        super().__init__()
        if not path.exists():
            msg = f"{path.resolve()} does not exist."
            raise FileNotFoundError(msg)
        self.path = path

    def perform(self, paste: Paste, analyzer_name: str | None = None, matches: list[re.Match] | None = None):
        if matches:
            # Append matches to file joined by newline
            with open(self.path, "+a", errors="ignore") as result_fp:
                result_fp.write("\n".join(matches) + "\n")


# Create PastePwn object
pastepwn = PastePwn()

# Check if result file exists and create if it doesnt
cc_path = Path("./credit_cards.txt")
if not cc_path.exists():
    cc_path.touch()

# Create analyzer object with action
cc_analyzer = CreditCardAnalyzer(AppendCCMatchFileAction(cc_path))

# Add analyzer to PastePwn
pastepwn.add_analyzer(cc_analyzer)

# Start PastePwn
pastepwn.start()
