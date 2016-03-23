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
        print msg['From']
        msg['To'] = receiver
        print msg['To']
        msg['Subject'] = subject
        print msg['Subject']
        if cc is not None:
            msg['Cc'] = cc
            print msg['Cc']
            # receiver += cc
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
        message = "Dear %s, <br>  \
            Compliance %s has assigned to you. Due date for the compliance is %s" % (
            assignee_name, compliance_name, due_date
        )
        self.send_email(receiver, subject, message)

    def notify_assign_compliance(self, receiver, assignee_name, compliance_info):
        subject = "New compliance task assigned "
        message = "Dear %s, <br> \
            <p>%s</p>" % (
            assignee_name, compliance_info,
        )
        print message
        self.send_email(receiver, subject, message)

    def notify_task(
        self, assignee_email, assignee_name, 
        concurrence_email, concurrence_name,
        approver_email, approver_name, compliance_name, 
        due_date, when
    ):
        receiver = "%s, %s, %s" % (assignee_email, concurrence_email, approver_email)
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
        self.send_email(receiver, subject, message)

    def notify_reassigned(self, receiver, reassigned_from, assignee, compliance_name, due_date):
        assignee_id, concurrence_id, approver_id,  compliance_name, document_name,  due_date = db.get_compliance_history_details(
            compliance_history_id
        )
        user_ids = "{},{},{}".format(assignee_id, concurrence_id, approver_id)
        receiver, employee_name = db.get_user_email_name(user_ids)
        cc = receiver.split(",")[2]
        if concurrence_id is not None or concurrence_id != 0:
            cc += ","+receiver.split(",")[1]
        if document_name is not None:
            compliance_name = "%s - %s" % (document_name, compliance_name)
        assignee_name = employee_name.split(",")[0]
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
        self, compliance_history_id, remarks, reject_status,
        assignee_name, assignee_email, concurrence_email,
        concurrence_name, compliance_name
    ):
        subject = "Task Rejected"
        message = "Dear %s, Compliance %s has been rejected. The reason is %s." % (
            assignee_name, compliance_name, remarks
        )
        receiver = assignee_email 
        cc = None
        if concurrence_email is not None and reject_status == "RejectApproval":
            cc = concurrence_email
        self.send_email(receiver, subject, message, cc)

    def notify_task_completed(
        self, assignee_email, assignee_name, concurrence_email, 
        concurrence_name, approver_email, approver_name, action,
        is_two_levels_of_approval, compliance_name
    ):
        approval_or_concurrence_person = approver_name
        approval_or_concurrence_email = approver_email
        if is_two_levels_of_approval and concurrence_name is not None:
            action = "concur"
            approval_or_concurrence_person = concurrence_name
            approval_or_concurrence_email = concurrence_email

        cc = "%s" % (assignee_email)
        subject = "Task Completed"
        message = '''
        Dear %s,
        <br>
        %s has completed the task %s successfully. Review and %s
        ''' % (
            approval_or_concurrence_person, assignee_name, compliance_name, action
        )
        self.send_email(approval_or_concurrence_email, subject, message, cc)

    def notify_task_approved(
        self, approval_status, assignee_name, assignee_email, 
        concurrence_name, concurrence_email, approver_name, approver_email,
        compliance_name, is_two_levels_of_approval
    ):

        subject = "Task %s" % approval_status
        message = '''
        Dear %s,
        <br>
        Task %s %s Successfully.
        ''' % (
            assignee_name, compliance_name, approval_status
        )
        cc = None
        if is_two_levels_of_approval and concurrence_email is not None:
            cc = concurrence_email
        self.send_email(assignee_email, subject, message, cc)
        if approval_status == "Concurred":
            cc = "%s" % (assignee_email)
            subject = "Task Concurred"
            message = '''
            Dear %s,
            <br>
            %s has completed the task %s successfully and %s has concurred the compliance.\
            Review and approve the compliance
            ''' % (
                approver_name, assignee_name , compliance_name,
                concurrence_name
            )
            self.send_email(approver_email, subject, message, cc)
