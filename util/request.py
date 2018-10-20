# -*- coding: utf-8 -*-
from threading import Lock
from requests import Session


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
            self.session = Session()
            self.proxies = proxies
            self._initialized = True

    def _request_wrapper(self, *args, **kwargs):
        headers = {
            "User-Agent": "pastepwn (https://github.com/d-Rickyy-b/pastepwn)"
        }
        response = self.session.request(headers=headers, proxies=self.proxies, *args, **kwargs)
        response_data = response.content.decode("utf-8")

        return response_data

    def get(self, url):
        return self._request_wrapper("GET", url)

    def post(self, url):
        return self._request_wrapper("POST", url)

    def put(self, url):
        return self._request_wrapper("PUT", url)

    def delete(self, url):
        return self._request_wrapper("DELETE", url)
