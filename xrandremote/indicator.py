from xrandremote.util import logger, get_icon, PKG_NAME
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk  # noqa
from gi.repository import AppIndicator3 as appindicator  # noqa

LOG = logger(__name__)


def create_callback(function, *default_args, **default_kwargs):
    def instantiate_callback(*args, **kwargs):
        default_args.extend(args)
        default_kwargs.update(**kwargs)
        return function(*default_args, **default_kwargs)

    return instantiate_callback


class IndicatorMenu(gtk.Menu):
    def __init__(self, callback, refresh):
        super(IndicatorMenu, self).__init__()
        self._callback = callback
        self._refresh = refresh
        self.entries = []
        self.update()
        self.static_setup()
        self._refresh(None)
        self.update()

    def static_setup(self):
        self.append(gtk.SeparatorMenuItem.new())

        refresh = gtk.MenuItem("Refresh")
        refresh.connect("activate", self._refresh)
        self.append(refresh)

        settings = gtk.MenuItem("Settings")
        # settings.connect("activate", window.on_show_origin)
        self.append(settings)

        about = gtk.MenuItem("About")
        # about.connect("activate", window.on_show_author)
        self.append(about)
        self.show_all()
        LOG.debug('showing all')

    def update(self, entries=[]):
        self.clear_entries()
        if not entries:
            none = gtk.MenuItem("None")
            none.set_sensitive(False)
            self.add_entry(none)
        for entry in entries:
            toggle_item = gtk.CheckMenuItem.new_with_label(entry)
            toggle_item.connect(
                'activate', create_callback(self._callback, entry=entry))
            self.add_entry(toggle_item)
        self.show_all()

    def add_entry(self, entry):
        self.insert(entry, len(self.entries))
        self.entries.append(entry)

    def clear_entries(self):
        for entry in self.entries:
            self.remove(entry)
        self.entries = []


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = appindicator.Indicator.new(
        PKG_NAME, get_icon('xrandremote-indicator.svg'),
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    menu = IndicatorMenu(callback=None, refresh=lambda x: True)
    indicator.set_menu(menu)
    gtk.main()


if __name__ == "__main__":
    main()
