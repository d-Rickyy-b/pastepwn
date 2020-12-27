# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import sys

from pastepwn.util import Request
from pastepwn.util import TemplatingEngine
from .basicaction import BasicAction

websockets_available = True
try:
    import websockets
except ImportError:
    websockets = None
    websockets_available = False


class DiscordAction(BasicAction):
    """Action to send a Discord message to a certain webhook or channel."""
    name = "DiscordAction"

    def __init__(self, webhook_url=None, token=None, channel_id=None, template=None):
        """Action to send a Discord message to a certain webhook or channel.
        Either the webhook parameter or the token & channel_id parameters are needed.

        1) You can setup a webhook in the discord server settings. A webhook is tied to one server & text channel
        > https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks


        2) Setup a discord bot (token) in the developer portal:
        > https://discordapp.com/developers/applications/
        After creating an app you can obtain the token by going to
        > https://discordapp.com/developers/applications/{your_app_id}/bot
        Format:
        > NTI5MzI1MzY4OTAyMDI1MjI3.DwvNFQ.5aNKUvYlAKqKKq6UJ1fRiARKNXQ

        3) Obtain the channel_id (18 digit number):
        > User Settings > Appearance > Enable Developer Mode and after that right click on any text channel to copy the ID

        :param webhook_url: The url obtained from the server settings
        :param token: A bot token obtained from the developer portal
        :param channel_id: The channel ID of a text channel you want to send messages into
        :param template: A template string describing how the paste variables should be filled in
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.bot_available = True

        if websockets is None or not websockets_available or (sys.version_info.major == 3 and sys.version_info.minor >= 10):
            self.logger.warning("Could not import 'websockets' module. So you can only use webhooks for discord.")
            self.bot_available = False

        self.webhook_url = webhook_url
        if webhook_url is None:
            # When there is no webhook_url, we need both token and channel_id
            if token is None or channel_id is None:
                raise ValueError("Invalid arguments: requires either webhook_url or token+channel_id arguments")

            if not self.bot_available:
                raise NotImplementedError("You can't use bot functionality without the 'websockets' module. Please import it or use webhooks!")

            self.token = token
            self.channel_id = channel_id
            self.identified = False

        self.template = template

    @asyncio.coroutine
    def _identify(self, ws_url):
        """Connect to the Discord Gateway to identify the bot."""
        # Docs: https://discordapp.com/developers/docs/topics/gateway#connecting-to-the-gateway
        # Open connection to the Discord Gateway
        if websockets is None:
            raise ImportError("Couldn't import websockets!")

        socket = yield from websockets.connect("{0}/?v=6&encoding=json".format(ws_url))
        try:
            # Receive Hello
            hello_str = yield from socket.recv()
            hello = json.loads(hello_str)
            if hello.get("op") != 10:
                self.logger.warning("[ws] Expected Hello payload but received %s", hello_str)

            # Send heartbeat and receive ACK
            yield from socket.send(json.dumps({"op": 1, "d": {}}))
            ack_str = yield from socket.recv()
            ack = json.loads(ack_str)

            # https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
            heartbeat_ack = 11
            if ack.get("op") != heartbeat_ack:
                self.logger.warning("[ws] Expected Heartbeat ACK payload but received %s", ack_str)

            # Identify
            payload = {
                "token": self.token,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "pastepwn",
                    "$device": "pastepwn"
                    }
                }
            yield from socket.send(json.dumps({"op": 2, "d": payload}))

            # Receive READY event
            ready_str = yield from socket.recv()
            ready = json.loads(ready_str)
            if ready.get("t") != "READY":
                self.logger.warning("[ws] Expected READY event but received %s", ready_str)
        finally:
            # Close websocket connection
            yield from socket.close()

    def initialize_gateway(self):
        """Initialize the bot token so Discord identifies it properly."""
        if self.webhook_url is not None:
            raise NotImplementedError("Gateway initialization is only necessary for bot accounts.")

        # Call Get Gateway Bot to get the websocket URL
        # https://discordapp.com/developers/docs/reference#authentication
        r = Request()
        r.headers = {"Authorization": "Bot {}".format(self.token)}
        res = json.loads(r.get("https://discordapp.com/api/gateway/bot"))
        ws_url = res.get("url")

        # Start websocket client
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._identify(ws_url))
        self.identified = True

    def perform(self, paste, analyzer_name=None, matches=None):
        """Send a message via Discord to a specified channel, without checking for errors"""
        r = Request()
        text = TemplatingEngine.fill_template(paste, analyzer_name, template_string=self.template, matches=matches)

        if self.webhook_url is not None:
            # Send to a webhook (no authentication)
            url = self.webhook_url
        else:
            # Send through Discord bot API (header-based authentication)
            url = "https://discordapp.com/api/channels/{0}/messages".format(self.channel_id)
            r.headers = {"Authorization": "Bot {}".format(self.token)}

        res = r.post(url, {"content": text})
        if res == "":
            # If the response is empty, skip further execution
            return

        res = json.loads(res)

        # https://discord.com/developers/docs/topics/opcodes-and-status-codes#json-json-error-codes
        unauthorized_code = 40001
        if res.get("code") == unauthorized_code and self.bot_available and self.webhook_url is None and not self.identified:
            # Unauthorized access, bot token hasn't been identified to Discord Gateway
            self.logger.info("Accessing Discord Gateway to initialize token")
            self.initialize_gateway()
            # Retry action
            self.perform(paste, analyzer_name=analyzer_name)
