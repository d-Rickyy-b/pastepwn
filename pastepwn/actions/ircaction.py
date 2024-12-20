import logging
import select
import socket
from queue import Empty, Queue
from threading import Event
from time import sleep

from pastepwn.util import TemplatingEngine
from pastepwn.util.threadingutils import join_threads, start_thread

from .basicaction import BasicAction

MAX_MSG_SIZE = 512


class IrcAction(BasicAction):
    """Action to send an irc message to a certain channel"""

    name = "IrcAction"

    def __init__(self, server=None, channel=None, port=6667, nick="pastepwn", template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self._msg_queue = Queue()
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

        self.server = server
        self.port = port
        self.nick = nick
        self.template = template

        if not channel.startswith("#"):
            channel = f"#{channel}"
        self.channel = channel

        # RFC1459 says that each message can only be 512 bytes including the CR-LF character
        self._max_payload_size = MAX_MSG_SIZE - len(f"PRIVMSG {channel}") - len("\r\n")

        self._exception_event = Event()
        self._stop_event = Event()

        self.logger.info("Starting up the IRC client - pastepwn can only send messages, as soon as the client is ready!")
        self._thread = start_thread(self._run_irc_client, "irc_client", exception_event=self._exception_event)

    def _run_irc_client(self):
        """Runs an IRC client, which handles sending messages and answering on Server PINGs.
        :return: None
        """
        # Connect to the IRC
        self._connect()
        self._login()
        self._join()

        while True:
            # Reference: https://hardmath123.github.io/socket-science-2.html
            data = ""
            readables, writables, exceptionals = select.select([self.ircsock], [self.ircsock], [self.ircsock])
            # When we got a readable socket, we read it's content
            if len(readables) == 1:
                data += self.ircsock.recv(MAX_MSG_SIZE).decode("UTF-8")

                if data == 0:
                    self.logger.error("The socket was disconnected!")
                    self._reconnect()

                # Split up the data in single IRC messages to handle them separately
                while "\r\n" in data:
                    message = data[: data.index("\r\n")]
                    data = data[data.index("\r\n") + 2 :]
                    self._handle_message(message)

            # We use the _stop_event to kill our thread
            if self._stop_event.is_set():
                break

            # As long as we are not connected, we don't want to send any messages
            if not self.connected:
                continue

            try:
                # We don't need to speed up message sending - We are only allowed 1 message every 2 seconds according to RFC 1459
                msg = self._msg_queue.get(True, 1)
            except Empty:
                continue

            self.logger.debug(f"New message on msg_queue: {msg}")
            self._send(f"PRIVMSG {self.channel} :{msg}")

    def _handle_message(self, message):
        """
        Handles IRC server messages
        :param message: A messare received from the IRC server
        :return:
        """
        self.logger.debug(f"Server message: {message}")
        words = message.split(" ")

        if message.startswith("PING"):
            self._pong()

        elif words[1] == "020" and not self.connected:
            # We connected our socket and now need to send our nick
            self._login()

        elif words[1] == "001" and not self.connected:
            # The server accepted our nick and sent us their MOTD. We now join a channel
            self.connected = True
            self._join()

        elif words[1] == "PRIVMSG" and words[2] == self.channel and "!status" in words[3] and self.connected:
            # A little gimmick to check the status of pastepwn via IRC
            self._send_message("Pastepwn is still functional and operating!")

    def _send(self, data):
        """
        Sends data to the IRC server over a socket
        :return: None
        """
        try:
            self.ircsock.send(bytes(f"{data}\r\n", "UTF-8"))
        except ConnectionAbortedError as e:
            self.logger.exception("Connection to IRC server lost")
            self._reconnect()

    def _reconnect(self):
        """
        Tries to reconnect to the IRC Server
        :return:
        """
        self.connected = False
        self._exception_event.set()

        while True:
            try:
                self._connect()
            except Exception:
                self.logger.exception("Exception while trying to connect to the IRC server occurred")
                self.logger.info("Sleeping for 10 seconds before trying next reconnect!")
                sleep(10)
            else:
                # No exception occurred - Our socket should be connected again
                return

    def _connect(self):
        """
        Connect to the IRC Server
        :return: None
        """
        self.logger.debug(f"Connecting to IRC server '{self.server}:{self.port}' using nick {self.nick}.")
        self.ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ircsock.connect((self.server, self.port))

    def _login(self):
        """
        Send login data to the IRC server
        :return:
        """
        self._send(f"NICK {self.nick}")
        self._send(f"USER {self.nick} 8 * :{self.nick}")

    def _join(self):
        """
        Joins an IRC channel
        :return: None
        """
        self.logger.debug(f"Joining channel '{self.channel}' on '{self.server}:{self.port}' using nick {self.nick}.")
        self._send(f"JOIN {self.channel}")

    def _quit(self, msg=None):
        """
        Quit from an IRC server
        :return: None
        """
        self.logger.info(f"Sending QUIT message to the server '{self.server}:{self.port}' from nick '{self.nick}'")
        if msg is not None and msg != "":
            msg = msg.replace("\r\n", " ").replace("\r", " ").replace("\n", " ")
            self._send(f"QUIT :{msg}")
        else:
            self._send("QUIT")

    def _pong(self):
        """
        Reply to a server PING with PONG
        :return: None
        """
        self.logger.debug("Server PING received. Replying to server with PONG.")
        self._send(f"PONG :{self.nick}")

    def _send_message(self, msg):
        """
        Sends a message to the specified IRC channel by putting it on the msg_queue
        Maximum sending frequency is 1 message every 2 seconds (according to RFC 1459)
        :param msg: String containing a message
        :return:
        """
        # We need to remove all newlines in a message, so that the whole message can be sent
        # because RFC 1459 defines CRLF as End of Message
        msg = msg.replace("\r\n", " ")
        msg = msg.replace("\r", " ")
        msg = msg.replace("\n", " ")
        if len(msg) > self._max_payload_size:
            # We need to split up the message into two parts and send it recursively
            self._send_message(msg[: self._max_payload_size])
            self._send_message(msg[self._max_payload_size :])
            return

        # Otherwise we can simply put it on the queue as a whole
        self._msg_queue.put(msg)

    def __del__(self):
        self._stop_event.set()
        join_threads([self._thread])

    def perform(self, paste, analyzer_name=None, matches=None):
        """Perform the action on the passed paste"""
        if self._exception_event.is_set():
            self.logger.error("The exception event is set. The IRC action might not perform as it should! Messages will be buffered for the case of a reconnect.")
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)
        self._send_message(text)
