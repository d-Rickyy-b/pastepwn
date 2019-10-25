# -*- coding: utf-8 -*-
import socket

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class IrcAction(BasicAction):
    """Action to send an irc message to a certain channel"""
    name = "IrcAction"
    irc = socket.socket()

    def __init__(
            self=None,
            server=None,
            channel=None,
            port=6667,
            nick="pastepwn"
    ):
        super().__init__()

        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.channel = channel
        self.port = port
        self.nick = nick

    def perform(self, paste, analyzer_name=None):
        """Perform the action on the passed paste"""
        if self.template is None:
            text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
        else:
            text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template)

        self.ircsock.connect((self.server, self.port))
        self.ircsock.send(bytes("USER " + self.nick + " " + self.nick + " " + self.nick + "n", "UTF-8"))
        self.ircsock.send(bytes("NICK " + self.nick + "n", "UTF-8"))
        self.ircsock.send(bytes("JOIN " + self.channel + "n", "UTF-8"))
        self.ircsock.send(bytes("PRIVMSG " + self.channel + " " + text + "n", "UTF-8"))
        self.ircsock.send(bytes("QUIT n", "UTF-8"))
