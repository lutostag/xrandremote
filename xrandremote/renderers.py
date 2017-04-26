import pulseaudio_dlna.plugins.upnp
import pulseaudio_dlna.plugins.chromecast
import pulseaudio_dlna.holder
import threading
from multiprocessing import Queue
from xrandremote.util import self_atomic


RENDERER_PLUGINS = [
    pulseaudio_dlna.plugins.upnp.DLNAPlugin(),
    pulseaudio_dlna.plugins.chromecast.ChromecastPlugin(),
]


class SafeHolder(pulseaudio_dlna.holder.Holder):
    @property
    @self_atomic('lock')
    def safe_devices(self):
        return self.devices.copy()


class RendererList(object):
    def __init__(self, queue):
        self.queue = queue
        self.__renderers = {}
        self.message_queue = Queue()
        self.lock = threading.Lock()

    @property
    @self_atomic('lock')
    def renderers(self):
        return self.__renderers.copy()

    @self_atomic('lock')
    def get_renderer(self, renderer_id):
        return self.__renderers[renderer_id]

    @self_atomic('lock')
    def __set_renderers(self, renderers):
        self.__renderers = renderers

    def refresh(self):
        holder = SafeHolder(plugins=RENDERER_PLUGINS,
                            message_queue=self.message_queue)
        holder.search(ttl=5)
        self.__set_renderers(holder.safe_devices)
