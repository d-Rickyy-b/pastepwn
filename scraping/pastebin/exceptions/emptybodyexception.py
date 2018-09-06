# -*- coding: utf-8 -*-


class EmptyBodyException(Exception):

    def __init__(self):
        super().__init__("The body of the response was empty")
