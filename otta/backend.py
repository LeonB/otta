import otta

class Backend(object):
	config = None
	service = None

	def __init__(self, config):
		self.config = config
		self.service = self.config.services[self.config.service]

	# Wanted to make this more decoupled but Pypubsub doesn't support
	@otta.utils.memoized
	def get_projects(self):
		return self.service.get_projects()

	@otta.utils.memoized
	def get_tasks(self, project):
		return self.service.get_tasks(project)

	def log_time(self, time, project = None, task = None):
		return self.service.log_time(time, project = project, task = task)
