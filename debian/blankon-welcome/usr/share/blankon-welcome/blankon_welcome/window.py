# window.py
#
# Copyright 2020 Herpiko Dwi Aguno
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import time
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib
import threading


@Gtk.Template(resource_path='/org/blankon/blankonWelcome/window.ui')
class BlankonWelcomeWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'BlankonWelcomeWindow'

    SkipBackButton = Gtk.Template.Child()
    NextButton = Gtk.Template.Child()
    Stacks = Gtk.Template.Child()

    SpinnerBox = Gtk.Template.Child()
    WelcomeBox = Gtk.Template.Child()
    MainBox = Gtk.Template.Child()
    SeeingBox = Gtk.Template.Child()
    HearingBox = Gtk.Template.Child()
    TypingBox = Gtk.Template.Child()
    PointingBox = Gtk.Template.Child()

    SeeingButton = Gtk.Template.Child()
    HearingButton = Gtk.Template.Child()
    TypingButton = Gtk.Template.Child()
    PointingButton = Gtk.Template.Child()

    SeeingMagnifierSwitch = Gtk.Template.Child()
    SeeingLargeTextSwitch = Gtk.Template.Child()
    SeeingHighContrastSwitch = Gtk.Template.Child()

    currentView = "welcome"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Stacks.set_visible_child(self.WelcomeBox)
        self.NextButton.connect("clicked", self.a11y)
        self.SkipBackButton.connect("clicked", self.do_skip_back)
        self.SeeingButton.connect("clicked", self.show_seeing_box)
        self.HearingButton.connect("clicked", self.show_hearing_box)
        self.TypingButton.connect("clicked", self.show_typing_box)
        self.PointingButton.connect("clicked", self.show_pointing_box)
        self.SeeingMagnifierSwitch.connect("state-set", self.toggle_magnifier)
        self.SeeingLargeTextSwitch.connect("state-set", self.toggle_large_text)
        self.SeeingHighContrastSwitch.connect("state-set", self.toggle_high_contrast)

        # Set default values
        setting = Gio.Settings.new("org.gnome.desktop.interface")
        current_value = setting.get_value("gtk-theme")
        print(current_value)
        if ("Contrast" in current_value.get_string()):
            self.SeeingHighContrastSwitch.set_active(True)

    def do_skip_back(self, button):
        if self.currentView == "welcome" or self.currentView == "a11y":
            self.NextButton.hide()
            self.SkipBackButton.hide()
            self.Stacks.set_visible_child(self.SpinnerBox)

            # Use threading to avoid blocking UI
            thread = threading.Thread(target=self.send_analytic)
            thread.daemon = True
            thread.start()
        else:
            self.Stacks.set_visible_child(self.MainBox)
            self.SkipBackButton.set_label("Finish")
            self.currentView = "a11y"

    def a11y(self, button):
        self.NextButton.hide()
        self.Stacks.set_visible_child(self.MainBox)
        self.SkipBackButton.set_label("Finish")
        self.currentView = "a11y"

    def show_seeing_box(self, button):
        self.SkipBackButton.show()
        self.currentView = "seeing"
        self.SkipBackButton.set_label("Back")
        self.Stacks.set_visible_child(self.SeeingBox)

    def show_hearing_box(self, button):
        self.SkipBackButton.show()
        self.currentView = "hearing"
        self.SkipBackButton.set_label("Back")
        self.Stacks.set_visible_child(self.HearingBox)

    def show_typing_box(self, button):
        self.SkipBackButton.show()
        self.currentView = "typing"
        self.SkipBackButton.set_label("Back")
        self.Stacks.set_visible_child(self.TypingBox)

    def show_pointing_box(self, button):
        self.SkipBackButton.show()
        self.currentView = "pointing"
        self.SkipBackButton.set_label("Back")
        self.Stacks.set_visible_child(self.PointingBox)

    def toggle_magnifier(self, switch, state):
        setting = Gio.Settings.new("org.gnome.desktop.a11y.applications")
        bool_value = GLib.Variant("b", state)
        setting.set_value("screen-magnifier-enabled", bool_value)

    def toggle_high_contrast(self, switch, state):
        setting = Gio.Settings.new("org.gnome.desktop.interface")
        default_value = setting.get_default_value("gtk-theme")
        current_value = setting.get_value("gtk-theme")
        high_contrast_value = GLib.Variant("s", "HighContrast")
        print(state)
        print(default_value)
        print(current_value)
        if (state):
            print(high_contrast_value)
            setting.set_value("gtk-theme", high_contrast_value)
        else:
            setting.set_value("gtk-theme", default_value)

    def toggle_large_text(self, switch, state):
        setting = Gio.Settings.new("org.gnome.desktop.interface")
        scale_value = GLib.Variant("d", 1.0)
        if (state):
            scale_value = GLib.Variant("d", 1.5)
        setting.set_value("text-scaling-factor", scale_value)

    def send_analytic(self):
        print("Send analytic data...")
        time.sleep(1)
        print("Data sent")
        self.close()
      
