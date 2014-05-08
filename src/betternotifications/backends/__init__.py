# -*- coding: utf-8 -*-
from backends.base import DummyBackend
from backends.email import EmailBackend
from backends.pushover import PushoverBackend


def get_backend(name):
	if name == "dummy":
		return DummyBackend
	elif name == "email":
		return EmailBackend
	elif name == "pushover":
		return PushoverBackend

	raise Exception("Unknown backend: %s" % name)