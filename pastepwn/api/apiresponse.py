# -*- coding: utf-8 -*-

import json


class APIResponse(object):

    def __init__(self, status, message):
        self.status = status
        self.message = message
        self.error = None

    def __str__(self):
        return json.dumps({"status": self.status, "error": self.error, "message": self.message})
