from jira.client import JIRA as JIRACLIENT
import otta

class JIRA(otta.Service):
	config = None
	connection = None

	def __init__(self, config):
		self.config = config

	def get_projects(self, projects = None):
		projects = {}
		for p in self.get_connection().projects():
			projects[p.name] = p

		return projects

	def get_tasks(self, project):
		tasks = {}
		for i in self.get_connection().search_issues('assignee = currentUser() AND project = %s' % project.id):
			subtasks = i.fields.subtasks

			# If there are subtasks: list them
			if len(subtasks) > 0:
				for subtask in subtasks:
					tasks["%s (%s)" % (i.fields.summary, subtask.fields.summary)] = subtask
			else:
				tasks[i.fields.summary] = i

		return tasks

	# time is in seconds
	def log_time(self, time, project = None, task = None):
		time = round(time/60)

		if time == 0:
			return False

		connection = self.get_connection()
		connection.add_worklog(task, "%im" % time)
		return True

	def get_connection(self):
		if not self.connection:
			self.connection = JIRACLIENT(options = {'server': self.config.services.JIRA.server}, basic_auth=(self.config.services.JIRA.username, self.config.services.JIRA.password))
		return self.connection
