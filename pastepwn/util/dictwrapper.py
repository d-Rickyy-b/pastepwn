# -*- coding: utf-8 -*-


# https://stackoverflow.com/questions/19799609/leaving-values-blank-if-not-passed-in-str-format
class DictWrapper(dict):
    def __missing__(self, key):
        return '{' + key + '}'
