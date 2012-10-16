import collections
import functools
import time
import threading
from gi.repository import Gtk

def get_class( kls ):
	parts = kls.split('.')
	module = ".".join(parts[:-1])
	m = __import__( module )
	for comp in parts[1:]:
		m = getattr(m, comp)
	return m

def format_seconds(seconds):
    return time.strftime('%H:%M', time.gmtime(seconds))

# http://python-gtk-3-tutorial.readthedocs.org/en/latest/dialogs.html
def warning_message(title, text):
    dialog = Gtk.MessageDialog(None, message_type = Gtk.MessageType.WARNING,
        buttons = Gtk.ButtonsType.CLOSE,
        text = title)
    dialog.format_secondary_text(text)
    dialog.run()
    dialog.destroy()

class memoized(object):
	'''Decorator. Caches a function's return value each time it is called.
	If called later with the same arguments, the cached value is returned
	(not reevaluated).
	'''
	def __init__(self, func):
		self.func = func
		self.cache = {}
	def __call__(self, *args):
		if not isinstance(args, collections.Hashable):
			# uncacheable. a list, for instance.
			# better to not cache than blow up.
			return self.func(*args)
		if args in self.cache:
			return self.cache[args]
		else:
			value = self.func(*args)
			self.cache[args] = value
			return value
	def __repr__(self):
		'''Return the function's docstring.'''
		return self.func.__doc__
	def __get__(self, obj, objtype):
		'''Support instance methods.'''
		return functools.partial(self.__call__, obj)

class RepeatTimer(threading.Thread):
	def __init__(self, interval, callback, args=[], kwargs={}):
		threading.Thread.__init__(self)
    		self.interval = interval
    		self.callback = callback
    		self.args = args
    		self.kwargs = kwargs
    		self.finished = threading.Event()

	def run(self):
		count = 0
		while not self.finished.is_set():
			self.finished.wait(self.interval)
			if not self.finished.is_set():
				self.callback(*self.args, **self.kwargs)

	def cancel(self):
		self.finished.set()
