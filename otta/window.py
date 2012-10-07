from gi.repository import Gtk

class Window(object):
	builder = None
	window = None

	def __init__(self, glade_file, window_name):
		#~ super(self.__class__, self).__init__()
		self.builder = Gtk.Builder()
		self.builder.add_from_file(glade_file)
		self.builder.connect_signals(self)

		self.window = self.get_widget(window_name)
		self.window.connect('delete-event', self.on_window_delete_event)

	def __getattr__(self, name):
		return getattr(self.window, name)

	def get_widget(self, name):
		""" skip one variable (huh) """
		return self.builder.get_object(name)
