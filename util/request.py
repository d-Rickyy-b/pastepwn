# -*- coding: utf-8 -*-
import certifi
import urllib3
from threading import Lock


class Request(object):
    _instance = None
    _lock = Lock()

    def __new__(cls):
        # override method to implement singleton
        # source: http://alacret.blogspot.com/2015/04/python-thread-safe-singleton-pattern.html
        if Request._instance is None:
            with Request._lock:
                if Request._instance is None:
                    Request._instance = super(Request, cls).__new__(cls)

        return Request._instance

    def __init__(self):
        self.http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

    def _request_wrapper(self, *args, **kwargs):
        headers = {
            "User-Agent": "pastepwn (https://github.com/d-Rickyy-b/pastepwn)"
        }
        response = self.http.request(headers=headers, *args, **kwargs)
        response_data = response.data.decode("utf-8")

        return response_data

    def get(self, url):
        return self._request_wrapper("GET", url)

    def post(self, url):
        return self._request_wrapper("POST", url)

    def put(self, url):
        return self._request_wrapper("PUT", url)

    def delete(self, url):
        return self._request_wrapper("DELETE", url)
