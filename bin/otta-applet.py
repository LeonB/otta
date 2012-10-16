#!/usr/bin/env python

from __future__ import print_function
from gi.repository import GLib
GLib.threads_init()
# from gi.repository import GObject
# GObject.threads_init()
from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import otta
import signal
import sys

class Otta_Appindicator(object):
    title = 'Online Time Tracking Applet'
    version = '0.0.1'
    icon_name = 'network-offline'

    menu = None
    number_of_minute_signals = 0

    def __init__(self):
        self.app = otta.App()
        self.setup_signaling()
        self.setup_callbacks(self.app)
        self.setup_menu(self.app)
        self.setup_appindicator()

        Gtk.main()

    def setup_signaling(self):
        signal.signal (signal.SIGINT, self.quit)
        signal.signal (signal.SIGSEGV, self.quit)

        # make Control-C work properly: fix for a stupid bug: https://bugzilla.gnome.org/show_bug.cgi?id=622084
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def setup_callbacks(self, app):
        app.timer.connect('started', self.on_timer_started)
        app.timer.connect('stopped', self.on_timer_stopped)
        app.timer.connect('paused', self.on_timer_paused)
        # self.timer.connect('second-signal', self.on_second_signal) #the constant activity on the bus prevents the power manager for doing it's job
        app.timer.connect('minute-signal', self.on_minute_signal)

    def setup_menu(self, app):
        builder = Gtk.Builder()
        builder.add_from_file("actions_menu.glade")
        self.menu = builder.get_object("menuActions")

        actions_menu = ActionsMenu(self, app, builder)
        builder.connect_signals(actions_menu)

    def setup_appindicator(self):
        self.indicator = appindicator.Indicator.new("example-simple-client", "indicator-messages", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_icon("media-playback-stop")
        # self.indicator.set_icon("/home/leon/.icons/Humanity/actions/22/media-playback-stop.png")
        self.indicator.set_label('00:00', '')
        self.indicator.set_menu(self.menu)

    def quit (self, *args):
        # Change this?
        for t in self.app.timer._timers:
            t.cancel()

        Gtk.main_quit()
        sys.exit()

    def on_timer_started(self, timer):
        self.indicator.set_icon("media-playback-start")
        # self.indicator.set_icon("/home/leon/.icons/Humanity/actions/22/media-playback-start.png")
        print('time(): %i' % self.app.timer.time())
        print('round_time(): %i' % self.app.timer.round_time())

    def on_timer_stopped(self, timer):
        self.indicator.set_icon("media-playback-stop")
        self.indicator.set_label('00:00', '')

        print(self.app.timer.time())
        print(self.app.timer.round_time())

    def on_timer_paused(self, timer):
        self.indicator.set_icon("media-playback-pause")

    def on_second_signal(self, timer, seconds):
        print('time: %i' % seconds)

    def on_minute_signal(self, timer, seconds):
        self.number_of_minute_signals = self.number_of_minute_signals + 1
        print('number of minute-signal: %i (%i seconds)' % (self.number_of_minute_signals, seconds))

        formatted_time = otta.utils.format_seconds(seconds)
        self.indicator.set_label(formatted_time, '')

class ActionsMenu(Gtk.Menu):
    def __init__(self, indicator, app, builder):
        self.app = app
        self.builder = builder
        self.timer_window = otta.windows.Timer(self.app)
        self.setup_labels()
        self.setup_callbacks()
        self.indicator = indicator

    def setup_labels(self):
        item = self.get_widget('menuitemIntegration')
        label = item.get_label()
        item.set_label(label % self.app.config.service)

    def setup_callbacks(self):
        self.app.timer.connect('started', self.on_timer_started)
        self.app.timer.connect('stopped', self.on_timer_stopped)
        self.app.timer.connect('paused', self.on_timer_paused)
        self.app.connect('current-task-changed', self.on_current_task_changed)

    def get_widget(self, name):
        """ skip one variable (huh) """
        return self.builder.get_object(name)

    # When the applet is clicked
    def on_menuActions_button_press_event(self, button, event):
        pass

    def left_click(self, event):
        pass

    def right_click(self, event):
        pass

    def on_menuitemStartTimer_activate(self, event):
        print('on_menuitemStartTimer_activate')
        self.app.timer.start()

    def on_menuitemPauseTimer_activate(self, event):
        if self.app.timer.state == otta.timer.STATE_PAUSED:
            self.app.timer.start()
        else:
            self.app.timer.pause()

    def on_menuitemStopTimer_activate(self, event):
        print('on_menuitemStopTimer_activate')
        self.app.timer.stop()
        self.app.save_current_timer()

    def on_menuitemResetTimer_activate(self, event):
        print('on_menuitemResetTimer_activate')

    def on_menuitemEditTimer_activate(self, event):
        print('on_menuitemEditTimer_activate')

    def on_menuitemRoundTime_activate(self, event):
        print('on_menuitemRoundTime_activate')

    def on_menuitemProjects_activate(self, event):
        print('on_menuitemProjects_activate')

    def on_menuitemIntegration_activate(self, event):
        print('on_menuitemIntegration_activate')

    def on_menuitemShowTimer_activate(self, event):
        print('on_menuitemShowTimer_activate')
        self.timer_window.show()

    def on_menuitemQuit_activate(self, event):
        print('on_menuitemQuit_activate')
        self.indicator.quit()

    def on_timer_started(self, timer):
        self.get_widget('menuitemStartTimer').hide()
        self.get_widget('menuitemStopTimer').show()
        self.get_widget('menuitemPauseTimer').show()
        self.get_widget('menuitemResetTimer').show()
        self.switch_pause_item()

    def on_timer_stopped(self, timer):
        self.get_widget('menuitemStartTimer').show()
        self.get_widget('menuitemStopTimer').hide()
        self.get_widget('menuitemPauseTimer').hide()
        self.get_widget('menuitemResetTimer').hide()

    def on_timer_paused(self, timer):
        self.switch_pause_item()

    def on_current_task_changed(self, app):
        if app.get_current_project() and app.get_current_task():
            self.enable_start_item()
        else:
            self.disable_start_item()

    def switch_pause_item(self):
        item = self.get_widget('menuitemPauseTimer')
        if self.app.timer.state == otta.timer.STATE_PAUSED:
            item.set_label('Resume')
        else:
            item.set_label('Pause')

    def enable_start_item(self):
        self.get_widget('menuitemStartTimer').set_sensitive(True)

    def disable_start_item(self):
        self.get_widget('menuitemStartTimer').set_sensitive(False)


# function to run/register the class
if __name__ == "__main__":
    try:
        Otta_Appindicator() # change to otta.app(): decouple appindicator
    except( KeyboardInterrupt ):
        sys.exit(0)

