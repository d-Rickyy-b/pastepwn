# -*- coding: utf-8 -*-


def listify(obj):
    """
    Make sure the given object is a list
    :param obj: Any object - either None, a list of objects or a single object
    :return: The given object formatted as list
    """
    if obj is None:
        # When the object is None, an empty list will be returned
        return []
    elif isinstance(obj, list):
        # When the object is already a list, that list will be returned
        return obj
    else:
        # When a single object is passed to the method, a list with the
        # object as single item will be returned
        return [obj]
