from gi.repository import Gtk
from gi.repository import GObject
import otta
from otta.models import Project, Task

class Timer(otta.Window):
	app = None
	projects = []

	def __init__(self, app):
		otta.Window.__init__(self, 'timer.glade', 'windowTimer')

		for project in self.get_projects():
			self.projects.append(project)

		self.app = app
		self.setup_completions()
		self.setup_project_widget()

	def setup_completions(self):
		self.setup_projects_completion()
		# self.setup_tasks_completion()

	# fill a liststore with project names
	def setup_projects_completion(self):
		widget = self.get_widget('entrycompletionProjects')
		widget.set_model(self.project_store())
		widget.set_match_func(self.full_text_search, None)

	# fill a liststore with task names
	def setup_tasks_completion(self):
		liststore = Gtk.ListStore(str)
		for task in self.app.backend.get_tasks():
			liststore.append([project])

		widget = self.get_widget('entrycompletionProjects')
		widget.set_model(liststore)
		widget.set_match_func(self.full_text_search, None)

	def setup_project_widget(self):
		project_widget = self.get_widget('comboboxProject')
		project_widget.set_model(self.project_store())

		renderer = project_widget.get_cells()[0]
		project_widget.set_cell_data_func(renderer, self.project_cell_data, None)

	def project_cell_data(self, widget, cell, liststore, iter, user_data):
		project = liststore.get_value(iter, 0)
		cell.set_property('text', project.title)

	def project_store(self):
		store = Gtk.ListStore(GObject.TYPE_PYOBJECT)
		for project in self.projects:
			store.append([project])

		return store

	def get_projects(self):
		for project in Project.select():
			yield project

	# Callback method for GtkEntryCompletion
	def full_text_search(self, completion, entrystr, iter, data):
		model = completion.get_model()
		modelstr = model[iter][0]
		return entrystr in modelstr

	def on_comboboxProject_changed(self, widget):
		print 'on_comboboxProject_changed'
		text = widget.get_active_text()
		projects = self.projects
		if text not in projects:
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
