from gi.repository import Gtk
from gi.repository import Gio
import otta
from otta.models import Project, Task

class Timer(otta.Window):
    app = None
    projects = []

    def __init__(self, app):
        otta.Window.__init__(self, 'timer.glade', 'windowTimer')

        self.window.set_keep_above(True)
        self.app = app
        self.setup_project_widget()
        self.setup_callbacks()

    def on_menuStartTimer(self):
        print 'asd'

    def setup_project_widget(self):
        widget = self.get_widget('comboboxProject')
        widget.set_model(self.project_store())

        completion = self.get_widget('entrycompletionProjects')
        completion.set_model(self.project_store())
        completion.set_match_func(self.full_text_search, None)

    def setup_callbacks(self):
        self.app.timer.connect('started', self.on_timer_started)
        self.app.timer.connect('stopped', self.on_timer_stopped)
        self.app.timer.connect('paused', self.on_timer_paused)
        self.app.timer.connect('minute-signal', self.on_minute_signal)
        self.app.connect('current-task-changed', self.on_current_task_changed)

    def project_store(self):
        store = Gtk.ListStore(str, int)
        for key, project in enumerate(self.app.projects):
            store.append([project.title, key])

        return store

    def setup_task_widget(self):
        widget = self.get_widget('comboboxTask')
        widget.set_model(self.task_store())

        completion = self.get_widget('entrycompletionTasks')
        completion.set_model(self.task_store())
        completion.set_match_func(self.full_text_search, None)

        # Empty the previous text / selected task
        entry = self.get_widget('comboboxTask-entry')
        entry.set_text('')

    def task_store(self):
        store = Gtk.ListStore(str, int)
        for key, task in enumerate(self.app.tasks):
            store.append([task.title, key])

        return store

    # Callback method for GtkEntryCompletion
    def full_text_search(self, completion, entrystr, iter, data):
        liststore = completion.get_model()
        modelstr = liststore[iter][0] # search column 0
        return entrystr.lower() in modelstr.lower()

    # When a project gets selected from the tasks popup (can be through 'on_project_match_selected')
    def on_comboboxProject_changed(self, widget):
        print 'on_comboboxProject_changed'
        tree_iter = widget.get_active_iter()
        self.disable_start_button()
        self.app.tasks = []

        if not tree_iter:
            self.app.set_current_task(None)
            self.setup_task_widget()
            return

        model = widget.get_model()
        key = model[tree_iter][1]
        self.app.set_current_project(self.app.projects[key])
        for t in self.app.get_current_project().tasks:
            self.app.tasks.append(t)
        self.setup_task_widget()

    # When a task gets selected from the tasks popup (can be through 'on_task_match_selected')
    def on_comboboxTask_changed(self, widget):
        print 'on_comboboxTask_changed'
        tree_iter = widget.get_active_iter()

        if not tree_iter:
            self.app.set_current_task(None)
            self.disable_start_button()
            return

        model = widget.get_model()
        key = model[tree_iter][1]
        self.app.set_current_task(self.app.tasks[key])

    # When a task gets selected from the projects completion popup
    def on_entrycompletionProjects_match_selected(self, widget, model, active_iter):
        key = model[active_iter][1] #get the 'key' column
        combo = self.get_widget('comboboxProject');
        combo.set_active_iter(combo.get_model().get_iter(key))

    # When a task gets selected from the tasks completion popup
    def on_entrycompletionTasks_match_selected(self, widget, model, active_iter):
        key = model[active_iter][1] #get the 'key' column
        combo = self.get_widget('comboboxTask');
        combo.set_active_iter(combo.get_model().get_iter(key))

    def on_window_delete_event(self, window, event):
        print 'on_window_delete_event'
        window.hide()
        # window.destroy()
        return True

    def on_buttonPlay_clicked(self, widget):
        if self.app.timer.state == otta.timer.STATE_STARTED:
            self.app.timer.stop()
            try:
                self.app.save_current_timer()
            except Exception as e:
                self.show_warning(e)
        else:
            self.app.timer.start()

    def on_timer_started(self, timer):
        self.set_stop_button()
        self.disable_comboboxes()

    def on_timer_stopped(self, timer):
        self.set_play_button()
        self.enable_comboboxes()
        self.set_label_time(0)

    def on_minute_signal(self, timer, seconds):
        self.set_label_time(seconds)

    def on_timer_paused(self, timer):
        self.set_play_icon()

    def on_current_task_changed(self, app):
        if app.get_current_project() and app.get_current_task():
            self.enable_start_button()
        else:
            self.disable_start_button()

    def enable_start_button(self):
        self.get_widget('buttonPlay').set_sensitive(True)

    def disable_start_button(self):
        self.get_widget('buttonPlay').set_sensitive(False)

    def enable_comboboxes(self):
        self.get_widget('comboboxProject').set_sensitive(True)
        self.get_widget('comboboxTask').set_sensitive(True)

    def disable_comboboxes(self):
        self.get_widget('comboboxProject').set_sensitive(False)
        self.get_widget('comboboxTask').set_sensitive(False)

    def set_label_time(self, seconds):
        formatted_time = otta.utils.format_seconds(seconds)
        label = self.get_widget('labelTime')
        label.set_label(formatted_time)

    def set_stop_button(self):
        image = self.get_widget('buttonPlayImage')
        icon, size = image.get_stock()
        image.set_from_stock(Gtk.STOCK_MEDIA_STOP, size)

        button = self.get_widget('buttonPlay')
        button.set_tooltip_text('Stop & save time')

    def set_play_button(self):
        image = self.get_widget('buttonPlayImage')
        icon, size = image.get_stock()
        image.set_from_stock(Gtk.STOCK_MEDIA_PLAY, size)

        button = self.get_widget('buttonPlay')
        button.set_tooltip_text('Start timer')

    def show_warning(self, message):
        # box = self.get_widget('boxWarning')
        # label = self.get_widget('labelWarning')
        # label.set_label('<b>%s</b>' % message)
        # box.show()
        otta.utils.warning_message('Warning', message)
