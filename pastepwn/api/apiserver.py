# -*- coding: utf-8 -*-
import asyncio
import logging
import socket
from threading import Event, Lock

from sanic import Sanic
from sanic.exceptions import NotFound

from pastepwn.util import start_thread
from .apiroutes import get_paste_by_id, get_pastes_by_date, scrape_paste, default, pastepwn, ignore_404s


# on linux we can use
# import uvloop


class APIServer(object):

    def __init__(self, host="0.0.0.0", port=8080, base_url="", exception_event=None):
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.is_running = False

        if base_url.endswith("/"):
            base_url = base_url[:-1]

        self.base_url = base_url
        self._server_lock = Lock()
        self._exception_event = exception_event or Event()
        self.loop = None
        self._api_thread = None
        self.app = Sanic("APIServer")

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))

        self._init_routes()

    def _init_routes(self):
        self._init_route(default, "/")
        self._init_route(get_paste_by_id, "/pastes/<pasteId>")
        self._init_route(get_pastes_by_date, "/pastes/findByDate")
        self._init_route(scrape_paste, "/pastes/scrape", methods=["POST"])
        self._init_route(pastepwn, "/pastepwn")
        self.app.error_handler.add(NotFound, ignore_404s)

    def _init_route(self, callback, path, methods=None):
        allowed_methods = methods or ["GET"]

        if path.startswith("/"):
            path = path[1:]

        self.app.add_route(callback, "{0}/{1}".format(self.base_url, path, methods=allowed_methods))

    def start(self):
        with self._server_lock:
            if self.is_running:
                return

            self._api_thread = start_thread(self._start_server, "sanicAPI", Event())
            self.is_running = True

    def stop(self):
        with self._server_lock:
            if not self.is_running:
                return

            try:
                self.loop.stop()
                self.logger.info("Stopping API Server!")
                self._api_thread.join()
                self.loop = None
                self.is_running = False
            except Exception as e:
                self.logger.error(e)

    def _start_server(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        server = self.app.create_server(sock=self.sock)
        self.loop = asyncio.get_event_loop()
        asyncio.ensure_future(server)

        try:
            self.loop.run_forever()
        except Exception as e:
            print(e)
            self.loop.stop()
