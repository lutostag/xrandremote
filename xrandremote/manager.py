import multiprocessing
from xrandremote.util import atomic
from xrandremote.display import Xrandr, Screen
from xrandremote.caster import Caster
from xrandremote.renderers import RendererList


class Manager(object):
    """This holds a mapping of:
    {remote_screen: Caster(screen, remote)}"""
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.rendererlist = RendererList()
        self.remotes = {}  # mapping of remote: screen

    @atomic
    def list_remotes(self):
        """List of remote displays"""
        return self.remotes.keys()

    @atomic
    def enable_remote(self, remote):
        screen = Xrandr.add_virtual()
        caster = Caster(screen, remote)
        self.remotes[remote] = caster
        caster.start()

    @atomic
    def disable_remote(self, remote):
        caster = self.remotes[remote]
        caster.stop()
        caster.screen.remove()

    @atomic
    def update_remotes(self):
        self.rendererlist.refresh()
        remote_screens = self.rendererlist.devices
        for remote, caster in self.remotes.items():
            if not caster:
                continue
            if remote not in remote_screens:
                caster.stop()
                caster.screen.remove()
                del self.remotes[remote]

        self.remotes = {remote: None for remote in remote_screens
                        if remote not in self.remotes}

    @atomic
    def update_locals(self):
        local_screens = Xrandr.screens()
        for remote, caster in self.remotes.items():
            if caster.screen not in local_screens:
                caster.update_resolution(local_screens.get(caster.screen))
