import ConfigParser
import os
import otta

class Config(object):
	services = None

	def __init__(self):
		self.services = Services()
		config = ConfigParser.ConfigParser()
		config.read(['otta.conf', os.path.expanduser('~/.config/otta.conf'), os.path.expanduser('~/.otta.conf'), '/etc/otta.conf'])

		for section in config.sections():
			# global section
			if section.lower() == 'global':
				obj = self

			# service section
			elif section.lower().startswith('service '):
				service = section[8:] # remove 'Service '

				# If the service doesn't exist in self.services: add it and instantiate it
				if service not in self.services:
					self.services[service] = otta.utils.get_class("otta.services.%s" % service)(self)

				# Get a pointer to self.services.SERVICE
				obj = self.services[service]

			# everything else: skip for now
			else:
				continue

			# For each key/value in config: add it to the object
			# If it exists (@property), make a _key
			for item in config.items(section):
				try:
					getattr(obj, item[0])
				except AttributeError:
					setattr(obj, item[0], item[1])
				else:
					setattr(obj, '_' + item[0], item[1])

	@property
	def round_time(self):
		if not hasattr(self, '_round_time'):
			return 0
		return float(self._round_time)


class Services(dict):
	def __getattr__(self, name):
		try:
			return self.__getitem__(name)
		except KeyError:
			return super(DictObj,self).__getattr__(name)
