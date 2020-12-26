# -*- coding: utf-8 -*-
import logging.handlers

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class SyslogAction(BasicAction):
    """Action to log a paste to the syslog"""
    name = "SyslogAction"

    def __init__(self, syslog_address="/dev/log", template=None):
        """
        This sets up a syslogger, which defaults to /dev/log.
        That means that it will work on most linux systems,
        but will not work on for example OSX.

        For OSX, the correct syslog address would be
        /var/run/syslog
        """
        super().__init__()
        self.template = template
        self.logger = logging.getLogger("SyslogLogger")
        self.logger.setLevel(logging.DEBUG)

        handler = logging.handlers.SysLogHandler(address=syslog_address)
        self.logger.addHandler(handler)

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Logs a paste to the syslog
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        :param matches: List of matches returned by the analyzer
        :return: None
        """
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)
        self.logger.debug(text)
