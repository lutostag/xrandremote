import os
import logging
import threading

PKG_NAME = 'xrandremote'
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL_LOCK = threading.Lock()


def logger(filename):
    relative = os.path.relpath(os.path.abspath(filename), start=TOP_DIR)
    location = os.path.join(PKG_NAME, relative)
    module_name = location.replace(os.sep, '.').rsplit('.', 1)[0]
    return logging.getLogger(module_name)


def get_icon(filename):
    icon_path = '../icons/scalable/'
    return os.path.join(TOP_DIR, icon_path, filename)


def atomic(func, lock=GLOBAL_LOCK):
    def run_func_atomically(*args, **kwargs):
        lock.acquire()
        value = func(*args, **kwargs)
        lock.release()
        return value
    return run_func_atomically


def self_atomic(lock_attr):
    def wrapper(func):
        def run_func_atomically(self, *args, **kwargs):
            getattr(self, lock_attr).acquire()
            value = func(self, *args, **kwargs)
            getattr(self, lock_attr).release()
            return value
        return run_func_atomically
    return wrapper
