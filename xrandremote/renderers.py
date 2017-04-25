import os
import pulseaudio_dlna.plugins.upnp
import pulseaudio_dlna.plugins.chromecast
import pulseaudio_dlna.holder
import threading
from multiprocessing import Queue
from xrandremote.util import atomic


RENDERER_PLUGINS = [
    pulseaudio_dlna.plugins.upnp.DLNAPlugin(),
    pulseaudio_dlna.plugins.chromecast.ChromecastPlugin(),
]


class SafeHolder(pulseaudio_dlna.holder.Holder):
    @property
    @atomic(self.lock)
    def safe_devices(self):
        return self.devices.copy()


class RendererList(object):
    def __init__(self, queue):
        self.queue = queue
        self.__renderers = {}
        self.message_queue = Queue()
        self.lock = threading.Lock()

    @property
    @atomic(self.lock)
    def renderers(self):
        return self.__renderers.copy()

    @atomic(self.lock)
    def get_renderer(self, renderer_id):
        return self.__renderers[renderer_id]

    @atomic(self.lock)
    def __set_renderers(self, renderers):
        self.__renderers = renderers

    def refresh(self):
        holder = pulseaudio_dlna.holder.Holder(
            plugins=RENDERER_PLUGINS, message_queue=self.message_queue)
        holder.search(ttl=5)
        self.__set_renderers(holder.devices)
