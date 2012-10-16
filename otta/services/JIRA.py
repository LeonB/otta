from jira.client import JIRA as JIRACLIENT
import otta

class JIRA(otta.Service):
	config = None
	connection = None

	def __init__(self, config):
		self.config = config

	def get_projects(self, projects = None):
		for p in self.get_connection().projects():
			yield {
				'id':      p.id,
				'title':   p.name,
				'service': 'JIRA'
			}

	def get_tasks(self):
		for task in self.get_connection().search_issues('assignee = currentUser()'):
			subtasks = task.fields.subtasks

			# If there are subtasks: list them
			if len(subtasks) > 0:
				for subtask in subtasks:
					yield {
						'id':         subtask.key, #DSS-17
						'title':      subtask.key + ' - %s: ' % task.fields.summary + subtask.fields.summary,
						'project_id': task.fields.project.id,
						'service':    'JIRA'
					}
			else:
				yield {
					'id':         task.key, #DSS-17
					'title':      task.key + ' - ' + task.fields.summary,
					'project_id': task.fields.project.id,
					'service':    'JIRA'
				}

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
