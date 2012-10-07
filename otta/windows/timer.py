from gi.repository import Gtk
import otta

class Timer(otta.Window):
	app = None

	def __init__(self, app):
		otta.Window.__init__(self, 'timer.glade', 'windowTimer')
		self.app = app
		self.setup_completions()

		project_widget = self.get_widget('comboboxProject')
		for project in self.app.backend.get_projects().keys():
			project_widget.append_text(project)

	def setup_completions(self):
		self.setup_projects_completion()
		# self.setup_tasks_completion()

	# fill a liststore with project names
	def setup_projects_completion(self):
		liststore = Gtk.ListStore(str)
		for project in self.app.backend.get_projects():
			liststore.append([project])

		widget = self.get_widget('entrycompletionProjects')
		widget.set_model(liststore)
		widget.set_match_func(self.full_text_search, None)

	# fill a liststore with task names
	def setup_tasks_completion(self):
		liststore = Gtk.ListStore(str)
		for task in self.app.backend.get_tasks():
			liststore.append([project])

		widget = self.get_widget('entrycompletionProjects')
		widget.set_model(liststore)
		widget.set_match_func(self.full_text_search, None)

	# Callback method for GtkEntryCompletion
	def full_text_search(self, completion, entrystr, iter, data):
		model = completion.get_model()
		modelstr = model[iter][0]
		return entrystr in modelstr

	def on_comboboxProject_changed(self, widget):
		print 'on_comboboxProject_changed'
		text = widget.get_active_text()
		projects = self.app.backend.get_projects()
		if not projects.has_key(text):
			return

		project = projects[text]

		task_widget = self.get_widget('comboboxTask')
		for task in sorted(self.app.backend.get_tasks(project).keys()):
			print task
			task_widget.append_text(task)

	def on_comboboxTask_changed(self, widget):
		print 'on_comboboxTask_changed'

	def on_window_delete_event(self, window, event):
		print 'on_window_delete_event'
		window.hide()
		return True

	def on_buttonPlay_clicked(self, window, event):
		print 'on_buttonPlay_clicked'
