# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlencode, urlsplit, urlunsplit


class BackendBase(object):

	def __init__(self, name, **kwargs):
		self.name = name
		self.extinfo_cgi = kwargs.get('extinfo_cgi', None)

	def send(self, alert, variables, subject, message, recipient):
		pass

	def get_extinfo_url(self, variables):
		if self.extinfo_cgi:
			scheme, netloc, path, query, fragment = urlsplit(self.extinfo_cgi)
			args = [
				('host', variables.get('HOSTALIAS'))
			]
			if variables.get('SERVICEDESC', None):
				args.append(('service', variables.get('SERVICEDESC', None)))

			args.append(('type', 1 if variables.get('SERVICEDESC', None) else 2))

			return urlunsplit((scheme, netloc, path, urlencode(args), fragment))


class DummyBackend(BackendBase):

	def send(self, alert, variables, subject, message, recipient):
		logging.info("Recipient: %s" % recipient)
		logging.info("Subject: %s" % subject)
		logging.info("Message: %s" % message)