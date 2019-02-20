# -*- coding: utf-8 -*-

import logging
from threading import Event, Lock

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

from pastepwn.util import start_thread

logger = logging.getLogger(__name__)


class APIServer(object):

    def __init__(self, port, app, ssl_ctx, exception_event=None):
        self.http_server = HTTPServer(app, ssl_options=ssl_ctx)
        self.port = port
        self.loop = None
        self.logger = logging.getLogger(__name__)
        self.is_running = False
        self.server_lock = Lock()
        self.shutdown_lock = Lock()
        self._exception_event = exception_event or Event()
        self._api_thread = None

    def start(self):
        if self.is_running:
            logger.warning("APIServer is already running!")
            return

        self._api_thread = start_thread(self._start, "pastepwnAPI", Event())

    def _start(self):
        with self.server_lock:
            IOLoop().make_current()
            self.is_running = True
            self.logger.debug('API Server started.')
            self.http_server.listen(self.port)
            self.loop = IOLoop.current()
            self.loop.start()
            self.logger.debug('API Server stopped.')
            self.is_running = False

    def stop(self):
        with self.shutdown_lock:
            if not self.is_running:
                self.logger.warning('API Server already stopped.')
                return
            else:
                # self.http_server.close_all_connections()
                # TODO Somehow the sockets keep existing which is why at some point there will
                # TODO be an OS error because the library tries to open another socked which already exists
                self.http_server.stop()
                self.loop.add_callback(self.loop.stop)

    def handle_error(self, request, client_address):
        """Handle an error gracefully."""
        self.logger.debug('Exception happened during processing of request from %s',
                          client_address, exc_info=True)


class APIAppClass(Application):

    def __init__(self, base_path="api"):
        handlers = [
            (r"/{0}/pastes/(.*)".format(base_path), PasteHandler)
        ]
        Application.__init__(self, handlers)


class PasteHandler(RequestHandler):
    SUPPORTED_METHODS = ["GET"]

    def __init__(self, application, request, **kwargs):
        super(PasteHandler, self).__init__(application, request, **kwargs)
        self.logger = logging.getLogger(__name__)

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def get(self, *args, **kwargs):
        # TODO Remove debug code
        print(self.path_args)
        self.set_status(200)
        logger.info(self.request.body)
        self.write("Hi")
