#!/usr/bin/python
import mandrill
from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from server.constants import (
    CLIENT_URL, KNOWLEDGE_URL
)


# server = smtplib.SMTP('mail.mindssoft.com', 25)
# server.ehlo()
# server.login(self.sender, self.password)

# msg = MIMEMultipart()
# msg['From'] = self.sender
# msg['To'] = receive
# msg['Subject'] = subject
# if cc is not None:
#     msg['Cc'] = cc
#     receiver += cc
# msg.attach(MIMEText(message, 'plain'))

# server.sendmail(self.sender, receiver,  msg.as_string())
# server.close()

__all__ = [
	"EmailHandler"
]

# CLIENT_URL = "http://localhost:8080/"
# KNOWLEDGE_URL= "http://localhost:8082/knowledge/"

class Email(object):

    def __init__(self):
        # self.sender = "compfie.saas@gmail.com"
        # self.password = "compfie@123"
        self.sender = "compfie.test@aparajitha.com"
        self.password = "Ctt@123"
        # self.API_KEY = 'u5IPdlY1JAxa5_fJoJaPEw'
        self.initializeTemplates()

    def send_email(self, receiver, subject, message, cc=None):
        print "inside send email"
        # server = smtplib.SMTP('smtp.gmail.com', 25, timeout=30)
        # server = smtplib.SMTP("mail.aparajitha.com", 465)
        # print server
        # server.ehlo()
        # server.starttls()
        # print server.login(self.sender, self.password)

        server = SMTP("mail.aparajitha.com", 465)
        print server
        server.set_debuglevel(False)
        server.login(self.sender, self.password)

        msg = MIMEMultipart()
        msg['From'] = self.sender
        msg['To'] = receiver
        msg['Subject'] = subject
        if cc is not None:
            msg['Cc'] = cc
            receiver += cc
        msg.attach(MIMEText(message, 'html'))
        print msg.as_string()
        response = server.sendmail(self.sender, receiver,  msg.as_string())
        print response
        server.close()

    def initializeTemplates(self):
        self.templates = {
            "task_rejected" : "TaskRejected",
            "task_completed" : "TaskCompleted",
            "reset_password" : "ResetPassword",
            "account_created" : "AccountCreated",
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
        # email_to = [receiver]
        # context = {
        #     "User" : db.get_user_name_by_id(user_id),
        #     "ResetLink" : reset_link
        # }
        # template_name = self.get_template("task_completed")
        user_name = db.get_user_name_by_id(user_id)
        user_name_parts = user_name.split("-")
        employee_name = user_name_parts[0]
        if len(user_name_parts) > 1:
            employee_name = user_name_parts[1]
        subject = "Reset Password"
        message = '''
            Dear %s, <br> \
            <p>Use the following link to reset your password</p>\
            <p>%s</p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
            employee_name, reset_link
        )
        self.send_email(receiver, subject, message, cc=None)
        # self.send_mail(template_name, email_to, context)
        return True

    def send_client_credentials(
        self, short_name, receiver, password
    ):
        subject = "Account Created"
        # message = "Dear Client, Your Compfie account has been created.\
        # Your Credentials are <br> Url: '%slogin/%s' <br> Username: %s <br> password: %s" % (
        # 	CLIENT_URL, short_name, receiver, password
        # )
        message = '''
            Dear Client, <br> \
            <p>Your Compfie account has been created. </p>\
            <p>Your login Credentials are: <br> \
            <p>Url: <a href='%slogin/%s'>%slogin/%s</a> \
            <br>Username: %s \
            <br>password: %s </p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
            CLIENT_URL, short_name, CLIENT_URL, short_name,
            receiver, password
        )
        self.send_email(receiver, subject, message)

    def send_user_credentials(
        self, short_name, receiver, password, employee_name, employee_code
    ):
        subject = "Account Created"
        # message = "Dear %s, Your Compfie account has been created. Your login credentials are: %s\
        # Url: '%slogin/%s' <br> Username: %s <br> password: %s" % (
        # 	CLIENT_URL, employee_name, employee_code, short_name, receiver, password
        # )
        message = '''
            Dear %s, <br> \
            <p>Your Compfie account has been created. </p>\
            <p>Your login Credentials are: <br> \
            <p>Url: <a href='%slogin/%s'>%slogin/%s</a> \
            <br>Username: %s \
            <br>password: %s </p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
            employee_name, CLIENT_URL, short_name, CLIENT_URL, short_name,
            receiver, password
        )
        self.send_email(receiver, subject, message)

    def send_knowledge_user_credentials(
        self, receiver, password, employee_name, employee_code
    ):
        subject = "Account Created"
        message = '''
            Dear %s, <br> \
            <p>Your Compfie account has been created. </p>\
            <p>Your login Credentials are: <br> \
            <p>Url: <a href='%s/login'>%s/login</a> \
            <br>Username: %s \
            <br>password: %s </p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
             employee_name, KNOWLEDGE_URL, KNOWLEDGE_URL, receiver, password
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

    def notify_assign_compliance(self, receiver, assignee_name, compliance_info):
        subject = "New compliance task assigned "
        message = "Dear %s, %s" % (
            assignee_name, compliance_info,
        )
        print message
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
        assignee_id, concurrence_id, approver_id, compliance_name, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
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
        # email_to = receiver.split(",")
        # context = {
        #     "User" : assignee,
        #     "Compliance" : compliance_name,
        #     "Reason" : rejected_reason
        # }
        # template_name = self.get_template("task_rejected")
        # self.send_mail(template_name, email_to, context)

    def notify_task_completed(
        self, db, compliance_history_id
    ):
        assignee_id, concurrence_id, approver_id, compliance_name, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        user_ids = "%s, %s" % (assignee_id, approver_id)
        action = "approve"
        if db.is_two_levels_of_approval() and concurrence_id != 0:
            user_ids = "%s, %s, %s" % (assignee_id, concurrence_id, approver_id)
            action = "concur"
        receiver, employee_name = db.get_user_email_name(user_ids)
        assignee = employee_name.split(",")[0]
        cc = "%s" % (receiver.split(",")[0])
        subject = "Task Completed"
        message = '''
        Dear %s,
        <br>
        %s has completed the task %s successfully. Review and %s
        ''' % (
            employee_name.split(',')[1], assignee , compliance_name, action
        )
        self.send_email(receiver.split(',')[1], subject, message, cc)

    def notify_task_approved(
        self, db, compliance_history_id, approval_status
    ):
        assignee_id, concurrence_id, approver_id, compliance_name, due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        user_ids = "%s, %s" % (assignee_id, approver_id)
        if db.is_two_levels_of_approval() and concurrence_id != 0:
            user_ids = "%s, %s, %s" % (assignee_id, concurrence_id, approver_id)
        receiver, employee_name = db.get_user_email_name(user_ids)
        assignee = employee_name.split(",")[0]
        subject = "Task %s" % approval_status
        message = '''
        Dear %s,
        <br>
        Task %s %s Successfully.
        ''' % (
            assignee, compliance_name, approval_status
        )
        cc = None
        if db.is_two_levels_of_approval() and concurrence_id != 0:
            cc = receiver.split(",")[1]
        self.send_email(receiver.split(",")[0], subject, message, cc)
        if approval_status == "Concurred":
            cc = "%s" % (receiver.split(",")[0])
            subject = "Task Concurred"
            message = '''
            Dear %s,
            <br>
            %s has completed the task %s successfully and %s has concurred the compliance.\
            Review and approve the compliance
            ''' % (
                employee_name.split(',')[2], assignee , compliance_name,
                employee_name.split(',')[1]
            )
            self.send_email(receiver.split(',')[2], subject, message, cc)
