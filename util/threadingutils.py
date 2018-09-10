# -*- coding: utf-8 -*-
from threading import Thread, current_thread


def _init_thread(self, target, name, *args, **kwargs):
    thr = Thread(target=self._thread_wrapper, name=name, args=(target,) + args, kwargs=kwargs)
    thr.start()


def _thread_wrapper(self, target, *args, **kwargs):
    thr_name = current_thread().name
    self.logger.debug('{0} - started'.format(thr_name))
    try:
        target(*args, **kwargs)
    except Exception:
        self.__exception_event.set()
        self.logger.exception('unhandled exception in %s', thr_name)
        raise
    self.logger.debug('{0} - ended'.format(thr_name))
