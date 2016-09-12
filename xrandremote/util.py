import os
import logging

PKG_NAME = 'xrandremote'
TOP_DIR = os.path.dirname(os.path.abspath(__file__))


def logger(filename):
    relative = os.path.relpath(os.path.abspath(filename), start=TOP_DIR)
    location = os.path.join(PKG_NAME, relative)
    module_name = location.replace(os.sep, '.').rsplit('.', 1)[0]
    return logging.getLogger(module_name)


def get_icon(filename):
    icon_path = '../icons/scalable/'
    return os.path.join(TOP_DIR, icon_path, filename)
