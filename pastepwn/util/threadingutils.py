# -*- coding: utf-8 -*-
import logging
from threading import Thread, current_thread


def start_thread(target, name, exception_event, *args, **kwargs):
    """
    Starts a thread passed as argument and catches exceptions that happens during execution
    :param target: Method to be executed in the thread
    :param name: Name of the thread
    :param exception_event: An event that will be set if an exception occurred
    :param args: Arguments to be passed to the threaded method
    :param kwargs: Keyword-Arguments to be passed to the threaded method
    :return:
    """
    thread = Thread(target=thread_wrapper, name=name, args=(target, exception_event) + args, kwargs=kwargs)
    thread.start()
    return thread


def thread_wrapper(target, exception_event, *args, **kwargs):
    """
    Wrapper around the execution of a passed method, that catches and logs exceptions
    :param target: Method to be executed
    :param exception_event: An event that will be set if an exception occurred
    :param args: Arguments to be passed to the target method
    :param kwargs: Keyword-Arguments to be passed to the target method
    :return:
    """
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


def join_threads(threads):
    """
    End all threads and join them back into the main thread
    :param threads: List of threads to be joined
    :return:
    """
    logger = logging.getLogger(__name__)
    for thread in threads:
        logger.debug("Joining thread {0}".format(thread.name))
        thread.join()
        logger.debug("Thread {0} has ended".format(thread.name))
