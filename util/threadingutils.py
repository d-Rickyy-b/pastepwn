# -*- coding: utf-8 -*-
from threading import Thread, current_thread
import logging


def start_thread(target, name, exception_event, *args, **kwargs):
    thread = Thread(target=thread_wrapper, name=name, args=(target, exception_event) + args, kwargs=kwargs)
    thread.start()


def thread_wrapper(target, exception_event, *args, **kwargs):
    thread_name = current_thread().name
    logger = logging.getLogger(__name__)
    logger.debug('{0} - thread started'.format(thread_name))
    try:
        target(*args, **kwargs)
    except Exception:
        exception_event.set()
        logger.exception('unhandled exception in %s', thread_name)
        raise
    logger.debug('{0} - thread ended'.format(thread_name))
