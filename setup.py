#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='better-notifications',
		version='0.1.1',
		description='Better notifications for Nagios/Icinga',
		author='Johann Schmitz',
		author_email='johann@j-schmitz.net',
		url='https://github.com/ercpe/better-notifications',
		packages=['betternotifications', 'betternotifications.backends'],
		package_dir={'': 'src'},
)
