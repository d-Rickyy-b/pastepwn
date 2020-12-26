# -*- coding: utf-8 -*-


class PastepwnError(Exception):
    """Representation of a pastepwn error object."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return str(self.message)


class InvalidActionError(PastepwnError):
    """Representation of an error for invalid actions passed to analyzers"""
    pass
