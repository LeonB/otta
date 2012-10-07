#!/usr/bin/env python

from gi.repository import Gtk
from gi.repository import AppIndicator3 as appindicator
import otta
import signal
import sys

class Otta_Appindicator():
	title = 'Online Time Tracking Applet'
	version = '0.0.1'
	icon_name = 'network-offline'

	backend = None
	config = None
	ind = None
	menu = None
	timer = None
	current_project = None
	curren_task = None

	def __init__(self):
		self.setup_signaling()
		self.setup_app()
		self.setup_menu()
		self.setup_appindicator()

		Gtk.main()

	def setup_signaling(self):
		signal.signal (signal.SIGINT, self.quit)
		signal.signal (signal.SIGSEGV, self.quit)

		# make Control-C work properly: fix for a stupid bug: https://bugzilla.gnome.org/show_bug.cgi?id=622084
		signal.signal(signal.SIGINT, signal.SIG_DFL)

	def setup_app(self):
		self.config = otta.Config()
		self.backend = otta.Backend(self.config)
		self.timer = otta.Timer(self.config)

	def setup_menu(self):
		builder = Gtk.Builder()
		builder.add_from_file("actions_menu.glade")
		self.menu = builder.get_object("menuActions")

		actions_menu = ActionsMenu(self)
		builder.connect_signals(actions_menu)

	def setup_appindicator(self):
		self.indicator = appindicator.Indicator.new("example-simple-client", "indicator-messages", appindicator.IndicatorCategory.APPLICATION_STATUS)
		self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		self.indicator.set_icon("media-playback-stop")
		self.indicator.set_label('00:00', '')
		self.indicator.set_menu(self.menu)

	def quit (self, *args):
		Gtk.main_quit()
		sys.exit()

class ActionsMenu(Gtk.Menu):
	def __init__(self, app):
		self.app = app
		self.timer_window = otta.windows.Timer(self.app)

	# When the applet is clicked
	def on_menuActions_button_press_event(self, button, event):
		pass

	def left_click(self, event):
		pass

	def right_click(self, event):
		pass

	def on_menuitemStartTimer_activate(self, event):
		print('on_menuitemStartTimer_activate')
		self.app.indicator.set_icon("media-playback-start")

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
		self.appindicator.quit()


# function to run/register the class
if __name__ == "__main__":
	try:
		Otta_Appindicator()
	except( KeyboardInterrupt ):
		sys.exit(0)

