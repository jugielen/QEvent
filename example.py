#!/usr/bin/env python

import gobject
import pygtk
pygtk.require('2.0')
import gtk
import time

class CalendarExample:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Calendar Example")
        window.set_border_width(5)
        window.set_size_request(200, 100)
        window.set_resizable(False)
        window.stick()
        window.connect("destroy", lambda x: gtk.main_quit())

        vbox = gtk.VBox(False, 10)
        window.add(vbox)

        # Could have used WINDOW_POPUP to create below window, but trying to emulate the same properties as the window
        # in applet.
        cal_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        cal_window.set_decorated(False)
        cal_window.set_resizable(False)
        cal_window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        cal_window.stick()
        cal_vbox = gtk.VBox(False, 10)
        cal_window.add(cal_vbox)
        cal_vbox.pack_start(gtk.Calendar(), True, False, 0)
        cal_vbox.pack_start(gtk.Button("Dummy locations"), True, False, 0)

        toggle_button = gtk.ToggleButton("Show Calendar")
        vbox.pack_start(toggle_button, False, True, 10)
        toggle_button.connect("toggled", self.on_toggle, cal_window)

        # Track movements of the window to move calendar window as well
        window.connect("configure-event", self.on_window_config, toggle_button, cal_window)
        window.show_all()