import logging
import threading
import pulseaudio_dlna.holder
import pulseaudio_dlna.plugins.upnp
import pulseaudio_dlna.plugins.chromecast


PLUGINS = [
    pulseaudio_dlna.plugins.upnp.DLNAPlugin(),
    pulseaudio_dlna.plugins.chromecast.ChromecastPlugin(),
]

logging.basicConfig()
pulseaudio_dlna.holder.logger.setLevel('DEBUG')
print(threading.enumerate())
holder = pulseaudio_dlna.holder.Holder(plugins=PLUGINS)
holder.search(ttl=5)
print(threading.enumerate())
holder.search(ttl=5)
print(threading.enumerate())
