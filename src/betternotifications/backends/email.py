# -*- coding: utf-8 -*-
from backends.base import BackendBase
from email.mime.text import MIMEText
import smtplib


class EmailBackend(BackendBase):

	def __init__(self, *args, **kwargs):
		super(EmailBackend, self).__init__(*args, **kwargs)
		self.server = kwargs.get('server', 'localhost')
		self.port = kwargs.get('port', 25)
		self.sender = kwargs.get('sender_address', 'noreply@localhost')

	def send(self, alert, variables, subject, message, recipient):
		msg = MIMEText(message)

		msg['Subject'] = subject

		if self.sender:
			msg['From'] = self.sender

		msg['To'] = recipient

		s = smtplib.SMTP(self.server, port=self.port)
		s.sendmail(self.sender, recipient, msg.as_string())
		s.quit()