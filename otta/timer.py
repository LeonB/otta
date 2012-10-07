import math
import time

class Timer(object):
	_time = 0
	config = None
	state = 'stopped'
	time_started = None
	time_stopped = 0

	def __init__(self, config):
		self.config = config

	def start(self):
		if self.state == 'started':
			return
		elif self.state == 'stopped':
			self._time = 0

		self._time_started = time.time()
		self.state = 'started'

	def stop(self):
		if self.state == 'stopped':
			return
		elif self.state == 'started':
			print 'registering stopped time'
			self.time_stopped = time.time()
			self._time = self._time + (self.time_stopped - self._time_started)

		self.state = 'stopped'

	def pause(self):
		if self.state != 'started':
			return

		self.time_stopped = time.time()
		self._time = self._time + (self.time_stopped - self._time_started)
		self.state = 'paused'

	def time(self):
		if self.state != 'started':
			return self._time

		return self._time + (time.time() - self._time_started)

	def round_time(self):
		time = self.time()
		units = time/(self.config.round_time*60)
		rounded_units = 0.0

		if self.config.round_method == 'down':
			rounded_units = math.floor(units)
		elif self.config.round_method == 'up':
			rounded_units = math.ceil(units)
		else:
			rounded_units = round(units)

		return int(rounded_units*(self.config.round_time*60))
