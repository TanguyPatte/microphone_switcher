#!/usr/bin/env python
import gi
import signal
import os
import dbus
import dbus.service
import dbus.glib
import subprocess
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

APPINDICATOR_ID = 'MicrophoneSwitcher'

class MicrophoneSwitcher:
    def __init__(self):
        self.enabled = self.is_microphone_enabled()
        dirname = os.path.dirname(os.path.abspath(__file__))
        self.enabled_icon = os.path.join(dirname, './microphone.png')
        self.disabled_icon = os.path.join(dirname, './no-microphone.png')
        self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, self.enabled_icon, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())


    def build_menu(self):
        menu = gtk.Menu()
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        item_switch = gtk.MenuItem('Switch')
        item_switch.connect('activate', self.switch_microphone_handler)
        menu.append(item_switch)
        menu.append(item_quit)
        menu.show_all()
        return menu


    def switch_microphone_handler(self,source):
        self.switch_microphone()


    def switch_microphone(self):
        self.toogle_microphone()
        if self.is_microphone_enabled():
            self.indicator.set_icon(self.enabled_icon)
        else:
            self.indicator.set_icon(self.disabled_icon)


    def is_microphone_enabled(self):
        process = subprocess.Popen(['amixer', 'get', 'Capture'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return '[on]' in stdout


    def toogle_microphone(self):
        subprocess.Popen(['amixer', 'set', 'Capture', 'toggle'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    def quit(self,source):
        gtk.main_quit()

class MicrophoneTooglerService(dbus.service.Object):

    def __init__(self, app):
        self.app = app
        bus_name = dbus.service.BusName(
            'org.tanguy.microphone_status', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/tanguy/microphone_status')


    @dbus.service.method(dbus_interface='org.tanguy.microphone_status')
    def capture_toogler(self):
        self.app.switch_microphone()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = MicrophoneSwitcher()
    service = MicrophoneTooglerService(app)
    gtk.main()
