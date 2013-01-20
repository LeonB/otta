import utils

from config import Config
from service import Service
from backend import Backend
from timer import Timer
from window import Window
import database
import services
import windows
import models

from gi.repository import GObject

class App(GObject.GObject):
    backend = None
    config = None
    ind = None
    timer = None
    _current_project = None
    _current_task = None
    projects = []
    tasks = []
    timer_started = None
    timer_stopped = None

    __gsignals__ = {
        'current-project-changed': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'current-task-changed':    (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self, *args):
    	GObject.GObject.__init__(self)
        self.config = Config()
        self.backend = Backend(self.config)
        self.timer = Timer(self.config)

        # get all projects
        for p in models.Project.select():
            self.projects.append(p)

    def set_current_project(self, project):
        self._current_project = project
        self.emit('current-project-changed')

    def get_current_project(self):
        return self._current_project

    def set_current_task(self, task):
        self._current_task = task
        self.emit('current-task-changed')

    def get_current_task(self):
        return self._current_task

    def save_current_timer(self):
        w = models.WorklogEntry()
        w.started_at = self.timer.started_at
        w.stopped_at = self.timer.stopped_at
        w.seconds = self.timer.time()
        w.task = self.get_current_task()

        print w.seconds
        if (w.seconds == 0):
            raise ValueError('A timer with %i seconds will not be saved' % w.seconds)

        w.save()
