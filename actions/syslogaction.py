# -*- coding: utf-8 -*-
import logging.handlers

from .basicaction import BasicAction


class SyslogAction(BasicAction):
    """Action to log a paste to the syslog"""
    name = "SyslogAction"

    def __init__(self, syslog_address="/dev/log"):
        """
        This sets up a syslogger, which defaults to /dev/log.
        That means that it will work on most linux systems,
        but will not work on for example OSX.

        For OSX, the correct syslog address would be
        /var/run/syslog
        """
        super().__init__()
        self.logger = logging.getLogger('SyslogLogger')
        self.logger.setLevel(logging.DEBUG)

        handler = logging.handlers.SysLogHandler(address=syslog_address)
        self.logger.addHandler(handler)

    def perform(self, paste, analyzer_name=None):
        self.logger.debug("New Paste matched: {0}".format(paste))
