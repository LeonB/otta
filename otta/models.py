import otta
import os
import peewee

class Project(peewee.Model):
	remote_id = peewee.CharField()
	title     = peewee.CharField()
	service   = peewee.CharField()
	# tasks     = peewee.ForeignKeyField(otta.models.Task, related_name='tasks')

	class Meta:
		database = peewee.SqliteDatabase(os.path.expanduser(otta.Config().database))

class Task(peewee.Model):
	remote_id         = peewee.CharField()
	title             = peewee.CharField()
	remote_project_id = peewee.CharField()
	service           = peewee.CharField()
	project           = peewee.ForeignKeyField(Project, related_name='tasks')

	class Meta:
		database = peewee.SqliteDatabase(os.path.expanduser(otta.Config().database))

class WorklogEntry(peewee.Model):
	date        = peewee.DateField()
	seconds     = peewee.IntegerField()
	description = peewee.TextField(null = True)
	task        = peewee.ForeignKeyField(Task, related_name='worklog_items')

	class Meta:
		database = peewee.SqliteDatabase(os.path.expanduser(otta.Config().database))
