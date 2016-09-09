import os
import logging

PKG_NAME = 'xrandremote'


def logger(filename):
    top_dir = os.path.dirname(os.path.abspath(__file__))
    relative = os.path.relpath(os.path.abspath(filename), start=top_dir)
    location = os.path.join(PKG_NAME, relative)
    module_name = location.replace(os.sep, '.').rsplit('.', 1)[0]
    return logging.getLogger(module_name)


def get_icon(filename):
    return '/home/lutostag/src/xrandremote/icons/scalable/xrandremote-indicator.svg'
