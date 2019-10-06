# -*- coding: utf-8 -*-
import asyncio
import json
import logging
import sys
from string import Template

from pastepwn.util import Request, DictWrapper
from .basicaction import BasicAction


class DiscordAction(BasicAction):
    """Action to send a Discord message to a certain webhook or channel."""
    name = "DiscordAction"

    def __init__(self, webhook=None, token=None, channel_id=None, template=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.bot_available = True

        try:
            import websockets
        except ImportError:
            self.logger.warning("Could not import 'websockets' module. So you can only use webhooks for discord.")
            self.bot_available = False

        self.webhook = webhook
        if webhook is None:
            if token is None or channel_id is None:
                raise ValueError('Invalid arguments: requires either webhook or token+channel_id arguments')

            if not self.bot_available:
                raise NotImplementedError("You can't use bot functionality without the 'websockets' module. Please import it or use webhooks!")

            self.token = token
            self.channel_id = channel_id
            self.identified = False

        if template is not None:
            self.template = Template(template)
        else:
            self.template = None

    @asyncio.coroutine
    def _identify(self, ws_url):
        """Connect to the Discord Gateway to identify the bot."""
        # Docs: https://discordapp.com/developers/docs/topics/gateway#connecting-to-the-gateway
        # Open connection to the Discord Gateway
        socket = yield from websockets.connect(ws_url + '/?v=6&encoding=json')
        try:
            # Receive Hello
            hello_str = yield from socket.recv()
            hello = json.loads(hello_str)
            if hello.get('op') != 10:
                self.logger.warning('[ws] Expected Hello payload but received %s', hello_str)
            
            # Send heartbeat and receive ACK
            yield from socket.send(json.dumps({"op": 1, "d": {}}))
            ack_str = yield from socket.recv()
            ack = json.loads(ack_str)
            if ack.get('op') != 11:
                self.logger.warning('[ws] Expected Heartbeat ACK payload but received %s', ack_str)

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
            if ready.get('t') != 'READY':
                self.logger.warning('[ws] Expected READY event but received %s', ready_str)
        finally:
            # Close websocket connection
            yield from socket.close()

    def initialize_gateway(self):
        """Initialize the bot token so Discord identifies it properly."""
        if self.webhook is not None:
            raise NotImplementedError('Gateway initialization is only necessary for bot accounts.')

        # Call Get Gateway Bot to get the websocket URL
        r = Request()
        r.headers = {'Authorization': 'Bot {}'.format(self.token)}
        res = json.loads(r.get('https://discordapp.com/api/gateway/bot'))
        ws_url = res.get('url')

        # Start websocket client
        asyncio.get_event_loop().run_until_complete(self._identify(ws_url))
        self.identified = True

    def perform(self, paste, analyzer_name=None):
        """Send a message via Discord to a specified channel, without checking for errors"""
        r = Request()
        if self.template is None:
            text = "New paste matched by analyzer '{0}' - Link: {1}".format(analyzer_name, paste.full_url)
        else:
            paste_dict = paste.to_dict()
            paste_dict["analyzer_name"] = analyzer_name
            text = self.template.safe_substitute(DictWrapper(paste_dict))

        if self.webhook is not None:
            # Send to a webhook (no authentication)
            url = self.webhook
        else:
            # Send through Discord bot API (header-based authentication)
            url = 'https://discordapp.com/api/channels/{0}/messages'.format(self.channel_id)
            r.headers = {'Authorization': 'Bot {}'.format(self.token)}

        res = r.post(url, {"content": text})
        if res == "":
            # If the response is empty, skip further execution
            return

        res = json.loads(res)

        if res.get('code') == 40001 and self.bot_available and self.webhook is None and not self.identified:
            # Unauthorized access, bot token hasn't been identified to Discord Gateway
            self.logger.info('Accessing Discord Gateway to initialize token')
            self.initialize_gateway()
            # Retry action
            self.perform(paste, analyzer_name=analyzer_name)
