#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import sys
import traceback
from config import BNConfigParser
from jinja2 import Template

def get_config():
	cfg = BNConfigParser()
	cfg.read(['backends.cfg', '/etc/better-notifications/backends.cfg'])

	return cfg


class Notifier(object):

	def __init__(self, template_dir, variables, alert_type, backend):
		self.template_dir = template_dir
		self.variables = variables
		self.backend = backend

		self.alert_type = alert_type
		if not self.alert_type:
			self.alert_type = 'service' if variables.get('SERVICEPROBLEMID', None) else 'host'
		logging.info("Sending a %s alert" % self.alert_type)

	def render(self, file):
		with open(file, 'r') as f:
			template = Template(f.read())
			return template.render(**self.variables)

	def notify(self, recipients):
		notification_type = self.variables.get('NOTIFICATIONTYPE', '').lower()

		message_templates = [
			os.path.join(self.template_dir, self.backend.name, "%s_%s.tpl" % (self.alert_type, notification_type)),
			os.path.join(self.template_dir, self.backend.name, "%s.tpl" % (notification_type, )),
			os.path.join(self.template_dir, self.backend.name, "%s.tpl" % (self.alert_type, )),
			os.path.join(self.template_dir, "%s_%s.tpl" % (self.alert_type, notification_type)),
			os.path.join(self.template_dir, "%s.tpl" % (notification_type, )),
			os.path.join(self.template_dir, "%s.tpl" % (self.alert_type, )),
			os.path.join(self.template_dir, "message.tpl"),
		]
		subject_templates = [
			os.path.join(self.template_dir, self.backend.name, "%s_%s_subject.tpl" % (self.alert_type, notification_type)),
			os.path.join(self.template_dir, self.backend.name, "%s_subject.tpl" % (notification_type, )),
			os.path.join(self.template_dir, self.backend.name, "%s_subject.tpl" % (self.alert_type, )),
			os.path.join(self.template_dir, "%s_%s_subject.tpl" % (self.alert_type, notification_type)),
			os.path.join(self.template_dir, "%s_subject.tpl" % (notification_type, )),
			os.path.join(self.template_dir, "%s_subject.tpl" % (self.alert_type, )),
			os.path.join(self.template_dir, "subject.tpl"),
		]

		logging.debug("Message templates: %s" % ', '.join(message_templates))
		logging.debug("Subject templates: %s" % ', '.join(subject_templates))

		message = ""
		subject = ""

		for f in message_templates:
			if os.path.exists(f):
				logging.info("Using template: %s" % f)
				message = self.render(f)
				break

		for f in subject_templates:
			if os.path.exists(f):
				logging.info("Using template: %s" % f)
				subject = self.render(f)
				break

		for recipient in recipients:
			self.backend.send(self.alert_type, self.variables, subject, message, recipient)


if __name__ == "__main__":
	config = get_config()

	parser = argparse.ArgumentParser()
	parser.set_defaults(prefix='ICINGA_')

	prefix_group = parser.add_mutually_exclusive_group()
	prefix_group.add_argument("--nagios", action="store_const", dest="prefix", const="NAGIOS_",
							  help="Use environmental variables prefixed with NAGIOS_")
	prefix_group.add_argument('--icinga', action="store_const", dest="prefix", const="ICINGA_",
							  help="Use environmental variables prefixed with ICINGA_ (default)")

	parser.add_argument('-a', '--alert', choices=('host', 'service'), help="The alert type to send (default: auto)")
	parser.add_argument('-b', '--backend', choices=config.get_backend_names(), required=True)
	parser.add_argument('-v', '--verbose', action='count', help="Increase verbosity", default=30)
	parser.add_argument('-t', '--template-dir', default="/etc/better-notifications/templates",
						help="Use templates from DIR instead of the default %(default)s")

	parser.add_argument('recipients', metavar='RECIPIENT', nargs='+', help='Backend-specific recipients (e.g. email adresses)')

	args = parser.parse_args()
	logging.basicConfig(level=50 - (int(args.verbose) * 10), format='%(levelname)-8s %(message)s')

	try:
		d = {}
		for k, v in os.environ.items():
			if not k.startswith(args.prefix):
				continue
			d[k[len(args.prefix):]] = v

		if not d:
			raise Exception("No environment variables found. Did you set environment_macros=true ?")

		if not Notifier(args.template_dir, d, args.alert, config.get_backend(args.backend)).notify(args.recipients):
			sys.exit(1)

	except Exception as ex:
		logging.error(ex)
		logging.error(traceback.format_exc())
		sys.exit(2)