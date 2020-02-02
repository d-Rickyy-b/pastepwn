# -*- coding: utf-8 -*-


# https://stackoverflow.com/questions/19799609/leaving-values-blank-if-not-passed-in-str-format
class DictWrapper(dict):
    """
    A wrapper around dicts which returns the key as string when missing.
    Used for the templating engine
    """

    def __missing__(self, key):
        return '${' + key + '}'
