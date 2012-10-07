#!/usr/bin/env python

import IPython
from IPython import embed
import otta

class Main(object):
	backend = None
	config = None
	project = None
	item = None
	timer = None

	def __init__(self):
		self.config = otta.Config()
		self.backend = otta.Backend(self.config)
		self.timer = otta.Timer(self.config)

	def start(self):
		if not self.project:
			raise Exception('No project set: pick one')

		if not self.item:
			raise Exception('No item set: pick one')

		self.timer.start()

	def pause(self):
		self.timer.pause()
		return "Timer paused"

	def stop(self):
		if not self.timer:
			raise Exception('No timer running')

		self.timer.stop()
		time = self.timer.round_time() #time is in seconds
		self.backend.log_time(time, project = self.project, item = self.item)

		print "Logged %i minutes" % round(time/60)

	def set_project(self, project):
		projects = self.get_projects()

		if isinstance(project, str):
			self.project = projects[project]
			project_name = project
		elif isinstance(project, int):
			self.project = projects.values()[project]
			project_name = projects.keys()[project]

		return "Setting '%s' as current project" % project_name

	def set_item(self, item):
		items = self.get_items()

		if isinstance(item, str):
			self.item = items[item]
			item_name = item
		elif isinstance(item, int):
			self.item = items.values()[item]
			item_name = items.keys()[item]

		return "Setting '%s' as current item" % item_name

	def get_projects(self):
		return self.backend.get_projects()

	def get_items(self):
		if not self.project:
			raise Exception('No current project set')

		return self.backend.get_items(self.project)

	def list_projects(self):
		projectlist = {}
		projects = self.get_projects()

		i = -1
		for pk in projects:
			i = i + 1
			projectlist[i] = pk

		return projectlist

	def list_items(self):
		itemlist = {}
		items = self.get_items()

		i = -1
		for pk in items:
			i = i + 1
			itemlist[i] = pk

		return itemlist


main = Main()
list_items = main.list_items
list_projects = main.list_projects
pause = main.pause
set_item = main.set_item
set_project = main.set_project
start = main.start
stop = main.stop
timer = main.timer

embed(header = 'asdasd')
