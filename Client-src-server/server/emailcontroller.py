
#!/usr/bin/python

# import mandrill
# from smtplib import SMTP_SSL as SMTP
import threading
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from server.constants import (
    CLIENT_URL, KNOWLEDGE_URL, SEND_EMAIL
)
__all__ = ["EmailHandler"]


class Email(object):

    def __init__(self):
        # self.sender = "compfie.saas@gmail.com"
        # self.password = "compfie@123"
        # self.sender = "compfie.test@aparajitha.com"
        # self.password = "Ctt@123"
        self.sender = "test@mindssoft.com"
        self.password = "Test$#4u"
        # self.API_KEY = 'u5IPdlY1JAxa5_fJoJaPEw'
        self.initializeTemplates()

    def send_email(
        self, receiver, subject, message, cc=None, is_credential=False
    ):
        print "inside send email"
        # server = smtplib.SMTP('smtp.gmail.com', 25, timeout=30)
        # server = smtplib.SMTP("mail.aparajitha.com", 465)
        # print server
        # server.ehlo()
        # server.starttls()
        # print server.login(self.sender, self.password)

        def send_sub_func(receiver, subject, message, cc=None, is_credential=False):
            print _is_send
            # server = SMTP("mail.aparajitha.com", 465)
            server = SMTP("smtp.mindssoft.com", 25)
            print server
            server.set_debuglevel(False)
            server.login(self.sender, self.password)

            msg = MIMEMultipart()
            print msg
            msg['From'] = self.sender
            print msg['From']
            if type(receiver) is list:
                msg['To'] = ",".join(receiver)
            else:
                msg['To'] = receiver
            print msg['To']
            msg['Subject'] = subject
            print msg['Subject']
            if cc is not None:
                if type(cc) is list:
                    msg['Cc'] = ", ".join(cc)
                else:
                    msg['Cc'] = cc
                print msg['Cc']
                # receiver += cc
            msg.attach(MIMEText(message, 'html'))
            print msg.as_string()
            final_receiver = receiver
            if cc is not None:
                if type(cc) is list:
                    if(type(receiver) is list):
                        final_receiver = receiver + cc
                    else:
                        final_receiver = cc + [receiver]
                else:
                    if(type(receiver) is list):
                        final_receiver = receiver + [cc]
                    else:
                        final_receiver = [receiver] + [cc]
            response = server.sendmail(
                self.sender, final_receiver,  msg.as_string()
            )
            print response
            server.close()

        _is_send = SEND_EMAIL
        if is_credential:
            _is_send = True
        if _is_send:
            begin_send = threading.Thread(
                target=send_sub_func,
                args=[receiver, subject, message, cc, is_credential]
            )
            begin_send.start()
        else:
            print "SEND_EMAIL is ", _is_send

    def initializeTemplates(self):
        self.templates = {
            "task_rejected": "TaskRejected",
            "task_completed": "TaskCompleted",
            "reset_password": "ResetPassword",
            "account_created": "AccountCreated",
        }

    def get_template(self, type):
        return self.templates[type]


class EmailHandler(Email):
    def __init__(
        self
    ):
        super(EmailHandler, self).__init__()

    def send_reset_link(
        self, db, user_id, receiver, reset_link, employee_name
    ):
        subject = "Reset Password"
        message = '''
            <p>Dear %s</p> \
            <p>Greetings from Compfie</p> \
            <p>You had recently requested to reset password  \
            for your Compfie Account. Click on the link given below to reset it.</p> \
            <p align="center">%s</p> \
            <p>We request you not to reveal your COMPFIE user id or password with others. \
            If you did not request a password reset, please ignore this email. \
            This password reset link is only valid for the next 24 hours. </p> \
            <p align="left">Thanks & regards,</p> \
            <p align="left">Compfie Administrator</p> \
        ''' % (employee_name, reset_link)
        # message = '''
        #     Dear %s, <br> \
        #     <p>Use the following link to reset your password</p>\
        #     <p>%s</p>\
        #     <p> Thanks & Regards, <br>\
        #     Compfie Support Team''' % (
        #     employee_name, reset_link
        # )
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )
        # self.send_mail(template_name, email_to, context)
        return True

    def send_registraion_link(
        self, receiver, employee_name, reset_link
    ):
        subject = "Confirm Your Registration"
        message = '''
            Dear %s, <br> \
            <p>Use the following link to confirm your registration </p>  <br>\
            <p>%s</p>  <br>\
            <p> Thanks & Regards, </p>  <br>\
            Compfie Support Team
        ''' % (employee_name, reset_link)
        self.send_email(receiver, subject, message, is_credential=True)

    def resend_registraion_link(
        self, receiver, reset_link
    ):
        subject = "Confirm Your Registration"
        message = '''
            Dear Group Admin, <br> \
            <p>Use the following link to confirm your registration </p>  <br>\
            <p>%s</p>  <br>\
            <p> Thanks & Regards, </p>  <br>\
            Compfie Support Team
        ''' % (reset_link)
        self.send_email(receiver, subject, message, is_credential=True)

    def send_notification_groupadmin_unit(
        self, receiver, group_name, legal_entity_name
    ):
        print "inside mail"
        subject = "Unit Creation Notification"
        message = '''
            Dear Group Admin, <br> \
            <p>For your kind information. </p>\
            <p>Unit(s) has been created for the below details :<br> \
            <br>Client Name: %s \
            <br>Legal Entity Name: %s </p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
            group_name, legal_entity_name)
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )
    
    def send_notification_groupadmin_statutory(
        self, receiver, group_name, legal_entity_name
    ):
        print "unit Creation mail"
        subject = "Statutory Assigned Notification"
        message = '''
            Dear Group Admin, <br> \
            <p>For your kind information. </p>\
            <p>Statutory has been assigned for the below details :<br> \
            <br>Client Name: %s \
            <br>Legal Entity Name: %s </p>\
            <p> Thanks & Regards, <br>\
            Compfie Support Team''' % (
            group_name, legal_entity_name)
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )

    def send_client_credentials(
        self, short_name, receiver, password
    ):
        subject = "Account Created"
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
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )

    def send_user_credentials(
        self, short_name, receiver, password, employee_name, employee_code
    ):
        subject = "Account Created"
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
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )

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
        self.send_email(
            receiver, subject, message, cc=None, is_credential=True
        )

    def notify_assign_compliance(
        self, receiver, assignee_name, compliance_info, cc=None
    ):
        subject = "New compliance task assigned "
        message = '''
            Dear %s, <br>
            <p>%s</p>''' % (
            assignee_name, compliance_info,
        )
        self.send_email(receiver, subject, message, cc)
    # On Occurrence Trigger
    # On Occurrence Task Reminder
    # Escalation for On Occurrence Task
    def notify_task(
        self, assignee_email, assignee_name,
        concurrence_email, concurrence_name,
        approver_email, approver_name, compliance_name,
        due_date, when
    ):
        receiver = "%s, %s, %s" % (
            assignee_email, concurrence_email, approver_email
        )
        if when == "Start":
            subject = "Task Started"

            message = '''
                <p>Dear %s</p>,
                %s
            ''' % (
                assignee_name, compliance_name
            )
        elif when == "Before Due Date":
            subject = "Task Reminder"
            message = '''
                <p>Dear %s</p>,
                %s
            ''' % (
                assignee_name, compliance_name
            )
        elif when == "After Due Date":
            subject = "Task Escalation"
            message = '''<p>Dear %s,</p>
                        %s
            ''' % (
                assignee_name, compliance_name
            )
        self.send_email(receiver, subject, message, cc=None)

    def notify_task_rejected(
        self, compliance_history_id, remarks, reject_status,
        assignee_name, assignee_email, concurrence_email,
        concurrence_name, compliance_name
    ):
        subject = "Task Rejected"
        message = '''
            Dear %s, Compliance %s has been rejected. The reason is %s.
        ''' % (
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
            approval_or_concurrence_person, assignee_name,
            compliance_name, action
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
                Dear %s,<br>
                %s has completed the task %s successfully and %s has concurred
                the compliance. Review and approve the compliance
            ''' % (
                approver_name, assignee_name, compliance_name,
                concurrence_name
            )
            self.send_email(approver_email, subject, message, cc)

    # for auto process
    def notify_compliance_start(
        self, assignee, compliance_name, unit_name,
        due_date, receiver, cc_person=None
    ):
        subject = "Compliance Task Started"
        message = '''
            Dear %s,
            Compliance task %s has been started for unit %s.
            Due date of this compliance is %s
        ''' % (
            assignee, compliance_name,
            unit_name, due_date
        )
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for compliance start ", message

    def notify_contract_expiration(
        self, receiver, content
    ):
        subject = "Contract expiration reminder"

        message = '''Dear Client, <br> <p>%s </p> \
                    <p> Thanks & Regards, <br>\
                    Compfie Support Team''' % content
        cc_person = None
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for compliance start ", message

    def notify_auto_deletion(
        self, receiver, content
    ):
        subject = "Deletion Alert"

        message = '''<p>%s </p> \
                    <p> Thanks & Regards, <br>\
                    Compfie Support Team''' % content
        cc_person = None
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for compliance start ", message
    # Escalation for On Occurrence Task
    def notify_to_assignee(
        self, assignee, days_left, compliance_name, unit_name,
        receiver
    ):
        subject = "Compliance Task Reminder"
        message = '''
            Dear %s, \
            Only %s day(s) left to complete %s task for unit %s
        ''' % (
            assignee, days_left, compliance_name, unit_name
        )
        try:
            print
            self.send_email(receiver, subject, message, cc=None)
            pass
        except Exception, e:
            print e
            print "Email Failed for notify to assignee %s ", message

    def notify_occurrence_to_assignee(
        self, assignee, days_left, compliance_name, unit_name,
        receiver
    ):
        subject = "Compliance Task Reminder"
        message = '''
            Dear %s, \
            Only %s left to complete %s task for unit %s
        ''' % (
            assignee, days_left, compliance_name, unit_name
        )
        try:
            print
            self.send_email(receiver, subject, message, cc=None)
            pass
        except Exception, e:
            print e
            print "Email Failed for notify to assignee %s ", message

    def notify_before_due_date(
        self, assignee, days_left, compliance_name, unit_name,
        receiver, cc_person
    ):
        subject = "Compliance Task Reminder"
        message = '''
            Dear %s, \
            Only %s day(s) left to complete %s task for unit %s
        ''' % (
            assignee, days_left, compliance_name,
            unit_name
        )
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for before due_date  ", message
    # Escalation for Periodical/Review/One Time Tasks after due date
    def notify_escalation(
        self, assignee, msg_text, receiver, cc_person
    ):
        subject = "Compliance Escalation Notification"
        message = '''
            Dear %s, \
             %s
        ''' % (
            assignee, msg_text
        )

        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for escalations", message
