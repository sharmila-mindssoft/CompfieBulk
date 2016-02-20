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

    def send_email(self, receiver, subject, message, cc=None):
        server = smtplib.SMTP('mail.mindssoft.com', 25)
        server.ehlo()
        server.login(self.sender, self.password)

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = receiver
        msg['Subject'] = subject
        if cc is not None:
            msg['Cc'] = cc
            receiver += cc
        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(self.sender, receiver,  msg.as_string())
        server.close()

    def initialize_templates():
        self.templates ={
        	"e" : "files/emailtemplates/emailtemplate.html"
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

    def notify_task(
        self, compliance_history_id, when
    ):
        assignee_id, concurrence_id, approver_id, compliance_name,  user_ids, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        receiver, employee_name = db.get_user_email_name(user_ids)
        cc = receiver.split(",")[2]
        if concurrence_id is not None or concurrence_id != 0:
            cc = receiver.split(",")[1]
        if when == "Start":
            subject = "Task Started"
            message = "Dear %s,  Compliance %s has started. Due date for the compliance is %s" % (
            	assignee_name, compliance_name, due_date
            )
        elif when == "Before Due Date":
            subject = "Task Reminder"
            message = "Dear %s, Reminding you to Complete the compliance %s with due date %s" % (
                assignee_name, compliance_name, due_date
            )
        elif when == "After Due Date":
            subject = "Task Escalation"
            message = "Dear %s, Compliance %s is delayed" % (
                assignee_name, compliance_name, due_date
            )
        self.send_email(receiver, subject, message, cc)

    def notify_reassigned(self, receiver, reassigned_from, assignee, compliance_name, due_date):
        assignee_id, concurrence_id, approver_id, compliance_name,  user_ids, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        receiver, employee_name = db.get_user_email_name(user_ids)
        cc = receiver.split(",")[2]
        if concurrence_id is not None or concurrence_id != 0:
            cc += receiver.split(",")[1]

        subject = "Task Started"
        message = "Dear %s,  compliance %s is reassigned to you from %s. Due date for the compliance is %s" % (
        	assignee_name, compliance_name, reassigned_from, due_date
        )
        self.send_email(receiver, subject, message, cc)

    def notify_service_provider_contract_expired(
        db, service_provider_id
    ):
        receiver = db.get_admin_username()
        service_provider_name = db.get_service_provider_name_by_id(service_provider_id)
        subject = "Contract Expired"
        message = "Dear Client, your contract with Service Provider %s has expired. \
        Kindly renew the contract" % (service_provider_name)
        self.send_email(receiver, subject, message)

    def notify_task_rejected(
        self, db, compliance_history_id, rejected_reason, reject_type
    ):
        result = db.get_compliance_history_details(
            compliance_history_id
        )
        assignee_id = result[0][0]
        concurrence_id = result[0][1]
        approver_id = result[0][2]
        compliance_name = result[0][3]
        due_date = result[0][4]
        user_ids = assignee_id
        if reject_type == "RejectApproval":
            if concurrence_id is None or concurrence_id == 0:
                user_ids = "%d,%d" % (user_ids, concurrence_id)

        receiver, employee_name = db.get_user_email_name(user_ids)
        assignee = employee_name.split(",")[0]
        subject = "Task Rejected"
        message = "Dear %s, Compliance %s has been rejected. The reason is %s." % (
            assignee, compliance_name, rejected_reason
        )
        sender = None
        cc = None
        if concurrence_id is not None and concurrence_id != 0:
            sender = receiver.split(",")[0]
            cc = receiver.split(",")[1]
        self.send_email(receiver, subject, message, cc)

    def notify_task_completed(
        self, db, compliance_history_id
    ):
        assignee_id, concurrence_id, approver_id, compliance_name,  user_ids, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        receiver, employee_name = db.get_user_email_name(user_ids)
        assignee = employee_name.split(",")[0]
        subject = "Task Completed"
        message = "Dear %s, Compliance %s has been completed. Verify and approve the compliance" % (
            assignee, compliance_name
        )
        sender = receiver.split(",")[2]
        cc = None
        if concurrence_id is not None and concurrence_id != 0:
            sender += receiver.split(",")[1]
            cc = receiver.split(",")[0]
        self.send_email(receiver, subject, message, cc)
