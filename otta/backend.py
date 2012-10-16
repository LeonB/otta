import otta
from otta.models import Project
from otta.models import Task

class Backend(object):
	config = None
	service = None

	def __init__(self, config):
		self.config = config
		self.service = self.config.services[self.config.service]

	def sync(self):
		self.sync_projects()
		self.sync_tasks()

	def sync_projects(self):
		service     = self.config.service
		project_ids = []

		for p in self.service.get_projects():
			project = self.sync_project(p)
			project_ids.append(project.id)

		Project.delete().where( \
			(Project.service == service) & \
			~(Project.id << project_ids) #NOT IN \
		).execute()

	def sync_project(self, project_dict):
		service = self.config.service

		try:
			project = Project.select().where(Project.remote_id == project_dict['id'], Project.service == service).get()
			if project.title != project_dict['title']:
				project.title = project_dict['title']
				project.save()
		except Project.DoesNotExist:
			project           = Project()
			project.remote_id = project_dict['id']
			project.title     = project_dict['title']
			project.service   = project_dict['service']
			project.save()

		return project

	def sync_tasks(self):
		service  = self.config.service
		task_ids = []

		for t in self.service.get_tasks():
			task = self.sync_task(t)
			task_ids.append(task.id)

		Task.delete().where( \
			(Task.service == service) & \
			~(Task.id << task_ids) #NOT IN \
		).execute()

	def sync_task(self, task_dict):
		project = None
		service = self.config.service

		try:
			task = Task.select().where(
				Task.remote_id == task_dict['id'],
				Task.service == service
			).get()

			if task.title != task_dict['title'] or task.remote_project_id != task_dict['project_id']:
				project                = Project.select().where(Project.remote_id == task_dict['project_id'], Project.service == service).get()
				task.title             = task_dict['title']
				task.remote_project_id = task_dict['project_id']
				task.project           = project
				task.save()
		except Task.DoesNotExist:
			project = Project.select().where(
				Project.remote_id == task_dict['project_id0'],
				Project.service == service
			).get()

			task                   = Task()
			task.remote_id         = task_dict['id']
			task.title             = task_dict['title']
			task.service           = task_dict['service']
			task.remote_project_id = task_dict['project_id']
			task.project           = project
			task.save()

		return task

	def log_time(self, time, project = None, task = None):
		return self.service.log_time(time, project = project, task = task)
