# -*- coding: utf-8 -*-
import logging
from threading import Lock
from requests import Session

from requests.exceptions import Timeout


class Request(object):
    _instance = None
    _initialized = False
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        # override method to implement singleton
        # source: http://alacret.blogspot.com/2015/04/python-thread-safe-singleton-pattern.html
        if Request._instance is None:
            with Request._lock:
                if Request._instance is None:
                    Request._instance = super(Request, cls).__new__(cls)
        return Request._instance

    def __init__(self, proxies=None):
        if not self._initialized:
            self.logger = logging.getLogger(__name__)
            self.session = Session()
            self.proxies = proxies
            self._initialized = True

    def _request_wrapper(self, timeout, *args, **kwargs):
        headers = {
            "User-Agent": "pastepwn (https://github.com/d-Rickyy-b/pastepwn)"
        }

        try:
            response = self.session.request(headers=headers, proxies=self.proxies, timeout=timeout, *args, **kwargs)
            response_data = response.content.decode("utf-8")
        except Timeout:
            self.logger.warning("Timeout while requesting {0}!".format(kwargs.get("url")))
            return ""

        return response_data

    def get(self, url, timeout=5):
        return self._request_wrapper(method="GET", url=url, timeout=timeout)

    def post(self, url, timeout=5):
        return self._request_wrapper(method="POST", url=url, timeout=timeout)

    def put(self, url, timeout=5):
        return self._request_wrapper(method="PUT", url=url, timeout=timeout)

    def delete(self, url, timeout=5):
        return self._request_wrapper(method="DELETE", url=url, timeout=timeout)
