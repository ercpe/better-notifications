# -*- coding: utf-8 -*-
import logging
from urllib.request import urlopen
from urllib.parse import urlencode, urlsplit, urlunsplit
from betternotifications.backends.base import BackendBase
import simplejson


class PushoverBackend(BackendBase):

	def __init__(self, *args, **kwargs):
		super(PushoverBackend, self).__init__(*args, **kwargs)
		self.api_token = kwargs.get('api_token')
		self.message_priority = kwargs.get('priority', 1)
		self.sound = kwargs.get('sound', None)
		self.extinfo_cgi = kwargs.get('extinfo_cgi', None)

	def send(self, alert, variables, subject, message, recipient):
		data = {
			'token': self.api_token,
			'user': recipient,
			'priority': self.message_priority,
			'sound': self.sound,
			'title': subject,
			'message': message,
		}

		if 'TIMET' in variables:
			data['timestamp'] = variables.get('TIMET')

		url = None

		if self.extinfo_cgi:
			scheme, netloc, path, query, fragment = urlsplit(self.extinfo_cgi)
			args = [
				('host', variables.get('HOSTALIAS'))
			]
			service_desc = variables.get('SERVICEDESC', None)
			if service_desc:
				args.append(('service', service_desc))

			data['url'] = urlunsplit((scheme, netloc, path, urlencode(args), fragment))

		try:
			logging.debug("Sending data: %s" % data)
			urlopen("https://api.pushover.net/1/messages.json",
						bytes(urlencode(data), encoding='utf-8'), timeout=15)
			return True
		except Exception as ex:
			logging.error("Pushover API request failed: %s" % ex)
			error_response = ex.fp.read()
			if error_response:
				error_obj = simplejson.loads(error_response)
				logging.error("Reason(s): %s" % ', '.join(error_obj['errors']))
			return False
