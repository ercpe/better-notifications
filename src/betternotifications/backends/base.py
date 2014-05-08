# -*- coding: utf-8 -*-
import logging


class BackendBase(object):

	def __init__(self, name, **kwargs):
		self.name = name

	def send(self, alert, variables, subject, message, recipient):
		pass


class DummyBackend(BackendBase):

	def send(self, alert, variables, subject, message, recipient):
		logging.info("Recipient: %s" % recipient)
		logging.info("Subject: %s" % subject)
		logging.info("Message: %s" % message)