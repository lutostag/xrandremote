import signal
from xrandremote.util import logger
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk as gtk  # noqa
from gi.repository import AppIndicator3 as appindicator  # noqa


APPINDICATOR_ID = 'xrandremote'


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, '/home/lutostag/src/xrandremote/icons/scalable/xrandremote-indicator.svg', appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    menu = gtk.Menu()
    none = gtk.MenuItem("None")
    none.set_sensitive(False)
    menu.append(none)

    toggle_item = gtk.CheckMenuItem.new_with_label('Enabled')
    menu.append(toggle_item)

    menu.append(gtk.SeparatorMenuItem.new())

    refresh = gtk.MenuItem("Refresh")
    # refresh.connect("activate", window.open_file)
    menu.append(refresh)

    settings = gtk.MenuItem("Settings")
    # settings.connect("activate", window.on_show_origin)
    menu.append(settings)

    about = gtk.MenuItem("About")
    # about.connect("activate", window.on_show_author)
    menu.append(about)
    menu.show_all()

    indicator.set_menu(menu)
    gtk.main()

if __name__ == "__main__":
    main()
