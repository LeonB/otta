from gi.repository import Gtk
from gi.repository import Gio
import otta
from otta.models import Project, Task

class Worklog(otta.Window):
    app = None

    def __init__(self, app):
        otta.Window.__init__(self, 'worklog.glade', 'windowWorklog')

        self.window.set_keep_above(True)
        self.app = app
        # self.setup_project_widget()
        self.setup_callbacks()

    def setup_callbacks(self):
    	pass

    def on_window_delete_event(self, window, event):
        print 'on_window_delete_event'
        window.hide()
        # window.destroy()
        return True
