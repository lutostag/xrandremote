import os
import pulseaudio_dlna.plugins.upnp
import pulseaudio_dlna.plugins.chromecast
import pulseaudio_dlna.holder


RENDERER_PLUGINS = [
    pulseaudio_dlna.plugins.upnp.DLNAPlugin(),
    pulseaudio_dlna.plugins.chromecast.ChromecastPlugin(),
]


def list_renderers():
    holder = pulseaudio_dlna.holder.Holder(plugins=RENDERER_PLUGINS)
    holder.search(ttl=5)
    return holder.devices
