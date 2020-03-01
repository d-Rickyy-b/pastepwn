# -*- coding: utf-8 -*-
import socket

from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction


class IrcAction(BasicAction):
    """Action to send an irc message to a certain channel"""
    name = "IrcAction"

    def __init__(self, server=None, channel=None, port=6667, nick="pastepwn", template=None):
        super().__init__()
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.channel = channel
        self.port = port
        self.nick = nick
        self.template = template

    def perform(self, paste, analyzer_name=None, matches=None):
        """Perform the action on the passed paste"""
        BUFF_SIZE = 1024
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches).replace("\r", "").replace("\n", "")
        # TODO RFC1459 says that each message can only be 512 bytes including the CR-LF character - this must be taken care of here
        # Currently we only cut off the text after 510 bytes (+CRLF = 512 bytes). It would be better to send all of text split up into multiple messages.
        text = text[:510]
        self.ircsock.connect((self.server, self.port))
        self.ircsock.send(bytes("NICK {}\r\n".format(self.nick), "UTF-8"))
        self.ircsock.send(bytes("USER {} {} bla :{}\r\n".format(self.nick, self.server, self.nick), "UTF-8"))
        self.ircsock.send(bytes("JOIN {}\r\n".format(self.channel), "UTF-8"))
        self.ircsock.send(bytes("PRIVMSG {} \r\n".format(self.channel, text), "UTF-8"))
        self.ircsock.send(bytes("QUIT\r\n", "UTF-8"))
        _ = self.ircsock.recv(BUFF_SIZE).decode("UTF-8")
        return
