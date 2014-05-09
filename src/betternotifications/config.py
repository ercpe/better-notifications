# -*- coding: utf-8 -*-

from configparser import ConfigParser
from betternotifications.backends import get_backend


class BNConfigParser(ConfigParser):

	def __init__(self, *args, **kwargs):
		super(BNConfigParser, self).__init__(*args, **kwargs)
		self._backends = None

	def get_backend(self, name):
		for b in self.get_backends():
			if b.name == name:
				return b

	def get_backend_names(self):
		return self.sections()

	def get_backends(self):
		if not self._backends:
			self._backends = []

			for name in self.sections():
				type = self.get(name, 'type')

				clazz = get_backend(type)

				d = dict(self.items(name))
				self._backends.append(clazz(name, **d))

		return self._backends