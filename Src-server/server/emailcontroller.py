#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# email_to = 'sharmila@mindssoft.com'
# username = 'sharmila@mindssoft.com'
# password = '6108816659'

# smtpserver = smtplib.SMTP("mindssoft.com",25)
# smtpserver.ehlo()
# smtpserver.login(username,password)
# header = 'To:' + <email_to + '\n' + 'From: ' + username + '\n' + 'Subject: Python SMTP Auth\n'
# msg = header + '\n\n This is a test message generated from python script \n\n'
# smtpserver.sendmail(username, email_to, msg)
# smtpserver.close()
# print 'Email sent successfully'

__all__ = [
	"EmailHandler"
]

class Email(object):
	
	def __init__(self):
		self.sender = "sharmila@mindssoft.com"
		self.password = "6108816659"

	def send_email(self, receiver, subject, message):
		server = smtplib.SMTP('mail.mindssoft.com', 25)
		server.ehlo()
		server.login(self.sender, self.password)

		msg = MIMEMultipart()
		msg['From'] = self.sender
		msg['To'] = receiver
		msg['Subject'] = subject
		msg.attach(MIMEText(message, 'plain'))

		server.sendmail(self.sender, receiver,  msg.as_string())
		server.close()

	def initialize_templates():
		self.templates ={
			"forgot_password" : "files/emailtemplates/forgot_password.html"
		}

	def get_template(self, type):
		return self.templates[type]

class EmailHandler(Email):
	def __init__(
        self
    ):
		super(EmailHandler, self).__init__()


	def send_reset_link(
		self, db, user_id, receiver, reset_link
	):
		subject = "Reset Password"
		message = "Dear User, Kindly click on the following link to reset your \
		password for Complify. %s" % reset_link 
		self.send_email(receiver, subject, message)
		return True

	def send_client_credentials(
		self, short_name, receiver, password
	):
		subject = "Account Created"
		message = "Dear Client, Your Compfie account has been created. Login and enjoy the services.\
		Your Credentials are <br> Url: 'http://localhost:8080/login/%s' <br> Username: %s <br> password: %s" % (
			short_name, receiver, password
		) 
		self.send_email(receiver, subject, message)

	def send_user_credentials(
        self, short_name, receiver, password, employee_name, employee_code
    ):
		subject = "Account Created"
		message = "Dear %s, Your Compfie account has been created. Your code is %s\
		Your Credentials are <br> Url: 'http://localhost:8080/login/%s' <br> Username: %s <br> password: %s" % (
			employee_name, employee_code, short_name, receiver, password
		) 
		self.send_email(receiver, subject, message)

	def send_knowledge_user_credentials(
        self, receiver, password, employee_name, employee_code
    ):
		subject = "Account Created"
		message = "Dear %s, Your Compfie account has been created. Your code is %s\
		Your Credentials are <br> Url: 'http://localhost:8082/knowledge/login' <br> Username: %s <br> password: %s" % (
			employee_name, employee_code,  receiver, password
		) 
		self.send_email(receiver, subject, message)

	def notify_task_assigned(
		self, receiver, assignee_name, compliance_name, due_date
	):
		subject = "Task Assigned"
		message = "Dear %s,  Compliance %s has assigned to you. Due date for the compliance is %s" % (
			assignee_name, compliance_name, due_date
		)
		self.send_email(receiver, subject, message)

	def notify_task_started(
		self, receiver, assignee_name, compliance_name, due_date
	):
		subject = "Task Started"
		message = "Dear %s,  Compliance %s has started. Due date for the compliance is %s" % (
			assignee_name, compliance_name, due_date
		)
		self.send_email(receiver, subject, message)

	def notify_reassigned(
		self, receiver, reassigned_from, assignee, compliance_name, due_date
	):
		subject = "Task Started"
		message = "Dear %s,  compliance %s is reassigned to you from %s. Due date for the compliance is %s" % (
			assignee_name, compliance_name, reassigned_from, due_date
		)
		self.send_email(receiver, subject, message)






