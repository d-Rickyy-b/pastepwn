# -*- coding: utf-8 -*-


class PastepwnError(Exception):
    """Representation of a pastepwn error object."""
    def __init__(self, message):
        """
        Initialize message

        Args:
            self: (todo): write your description
            message: (str): write your description
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        """
        Return a human - readable string representation.

        Args:
            self: (todo): write your description
        """
        return '%s' % self.message


class InvalidActionError(PastepwnError):
    """Representation of an error for invalid actions passed to analyzers"""
    pass
