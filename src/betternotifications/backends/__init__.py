# -*- coding: utf-8 -*-
from betternotifications.backends.base import DummyBackend
from betternotifications.backends.email import EmailBackend
from betternotifications.backends.pushover import PushoverBackend


def get_backend(name):
	if name == "dummy":
		return DummyBackend
	elif name == "email":
		return EmailBackend
	elif name == "pushover":
		return PushoverBackend

	raise Exception("Unknown backend: %s" % name)