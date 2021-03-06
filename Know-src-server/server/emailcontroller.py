
#!/usr/bin/python

# import mandrill
# from smtplib import SMTP_SSL as SMTP
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from server.constants import (
    CLIENT_URL, KNOWLEDGE_URL, SEND_EMAIL
)
__all__ = ["EmailHandler"]


class Email(object):

    def __init__(self):
        self.sender = "test@mindssoft.com"
        self.password = "Test$#4u"
        self.initializeTemplates()

    def send_email(
        self, receiver, subject, message, cc=None, is_credential=False
    ):
        _is_send = SEND_EMAIL
        if is_credential:
            _is_send = True
        if _is_send:
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

    # Forgot Password
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
        return True
    # Registration Mail & Resend Regn Mail
    def send_registraion_link(
        self, receiver, employee_name, reset_link
    ):
        # User Registration email
        subject = "Confirm Your Registration"
        message = '''
            <p>Dear Admin,</p> \
            <p>Welcome to Compfie</p> \
            <P>We are very happy to have you in our clientele portfolio</P>  \
            <p>Compfie is a cloud based software which will facilitate you to \
            assign, track, check and ensure the compliance status of your Company \
            irrespective of the number of entities you have, the volume of your \
            branches and your presence in various locations across India.</p> \
            <p>Compfie is a unique and comprehensive solution for all the entities \
            falling under various segments of Industries and it offers a great \
            comfort in tracking, monitoring the progress of all your statutory \
            compliance related tasks.</p> \
            <P>You can access the software on the go whether you are on \
            travel or on vacation, all you have to do is to login in our \
            portal to check, trigger and be compliant at any time.</P> \
            <p>Through Compfie you can generate reports both in Graphical \
             representations and Excel format as follows;</p> \
            <ul> \
            <li>A well-defined Dashboard to meet up all your requirements for board presentations</li> \
            <li>Group/Entity wise Compliance Report- Ensure all compliances are defined & none is missed.</li> \
            <li>Entity wise Report- Location Wise Pending due and overdue compliances.</li> \
            <li>Act Wise Report- Statutory Act wise Compliance Task reports.</li> \
            <li>And many other reports which are required for administering Compliances</li> \
            <li>All the above reports could be further drilled down  \
            using various filter options as per the necessity</li> \
            </ul> \
            <p>You may please go through the User Manual and Standard \
            Operation Procedures to get to know more about Compfie.</p> \
            <p>To complete the registration process, please click on the \
            link given below or copy-paste the link in your browser to \
            create your unique user id and password for Compfie.</p> \
            <p align="center">%s</p>
            <p align="left">Regards</p>
            <p align="left">Compfie Administrator</p>
        ''' % (reset_link)
        print message
        # message = '''
        #     Dear %s, <br> \
        #     <p>Use the following link to confirm your registration </p>  <br>\
        #     <p>%s</p>  <br>\
        #     <p> Thanks & Regards, </p>  <br>\
        #     Compfie Support Team
        # ''' % (employee_name, reset_link)
        self.send_email(receiver, subject, message, is_credential=True)

    def resend_registraion_link(
        self, receiver, reset_link
    ):
        # Group admin user registration email
        subject = "Confirm Your Registration"
        message = '''
            <p>Dear Admin,</p> \
            <p>Welcome to Compfie</p> \
            <P>We are very happy to have you in our clientele portfolio</P>  \
            <p>Compfie is a cloud based software which will facilitate you to \
            assign, track, check and ensure the compliance status of your Company \
            irrespective of the number of entities you have, the volume of your \
            branches and your presence in various locations across India.</p> \
            <p>Compfie is a unique and comprehensive solution for all the entities \
            falling under various segments of Industries and it offers a great \
            comfort in tracking, monitoring the progress of all your statutory \
            compliance related tasks.</p> \
            <P>You can access the software on the go whether you are on \
            travel or on vacation, all you have to do is to login in our \
            portal to check, trigger and be compliant at any time.</P> \
            <p>Through Compfie you can generate reports both in Graphical \
             representations and Excel format as follows;</p> \
            <ul> \
            <li>A well-defined Dashboard to meet up all your requirements for board presentations</li> \
            <li>Group/Entity wise Compliance Report- Ensure all compliances are defined & none is missed.</li> \
            <li>Entity wise Report- Location Wise Pending due and overdue compliances.</li> \
            <li>Act Wise Report- Statutory Act wise Compliance Task reports.</li> \
            <li>And many other reports which are required for administering Compliances</li> \
            <li>All the above reports could be further drilled down  \
            using various filter options as per the necessity</li> \
            </ul> \
            <p>You may please go through the User Manual and Standard \
            Operation Procedures to get to know more about Compfie.</p> \
            <p>To complete the registration process, please click on the \
            link given below or copy-paste the link in your browser to \
            create your unique user id and password for Compfie.</p> \
            <p align="center">%s</p>
            <p align="left">Regards</p>
            <p align="left">Compfie Administrator</p>
        ''' % (reset_link)
        # message = '''
        #     Dear Group Admin, <br> \
        #     <p>Use the following link to confirm your registration </p>  <br>\
        #     <p>%s</p>  <br>\
        #     <p> Thanks & Regards, </p>  <br>\
        #     Compfie Support Team
        # ''' % (reset_link)
        print message
        print reset_link
        self.send_email(receiver, subject, message, is_credential=True)
    # Unit Creation Mail
    def send_notification_groupadmin_unit(
        self, receiver, group_name, legal_entity_name
    ):
        print "inside mail"
        subject = "Unit Creation Notification"
        message = '''
            <p>Dear Admin,</p> \
            <p>Greetings from Compfie</p> \
            <p>Please be informed that the Units have been created \
            for the "%s" as per the list received from your \
            end along with the agreement. You may start creating Users \
            through "Login>>Masters>>User Management". \
            Please note that you have to set the privilege of each user \
            group before creating the Users. The same can be set through \
            "Login>>Masters>>User Privilege".</p> \
            <p>Customization of Statutes are under process and we \
            shall let you know on the completion shortly.</p> \
            <p align="left">Thanks & regards,</p> \
            <p align="left">Compfie Administrator</p> \
        ''' % (legal_entity_name)
        print message
        # message = '''
        #     Dear Group Admin, <br> \
        #     <p>For your kind information. </p>\
        #     <p>Unit(s) has been created for the below details :<br> \
        #     <br>Client Name: %s \
        #     <br>Legal Entity Name: %s </p>\
        #     <p> Thanks & Regards, <br>\
        #     Compfie Support Team''' % (
        #     group_name, legal_entity_name)
        self.send_email(
            receiver, subject, message, is_credential=True
        )

    # Assign Statutory Mail
    def send_notification_groupadmin_statutory(
        self, receiver, group_name, legal_entity_name
    ):
        print "unit Creation mail"
        subject = "Statutory Assigned Notification"
        message = '''
            <p>Dear Admin,</p> \
            <p>Greetings from Compfie</p> \
            <p>Please be informed that the applicability of statutes have been mapped  \
            for the set of units falls under "%s". You are free to either \
            opt in or opt out of the statutes mapped for each unit through \
            "Login>>Transactions>>Statutory Settings".  On successful completion of \
             Statutory Settings, you may start assigning the Compliance Tasks to your assignees.</p> \
            <p>Always keep on track of reminders, messages, \
            escalations and statutory notifications and stay compliant.</p> \
            <p align="left">Thanks & regards,</p> \
            <p align="left">Compfie Administrator</p> \
        ''' % (legal_entity_name)
        # message = '''
        #     Dear Group Admin, <br> \
        #     <p>For your kind information. </p>\
        #     <p>Statutory has been assigned for the below details :<br> \
        #     <br>Client Name: %s \
        #     <br>Legal Entity Name: %s </p>\
        #     <p> Thanks & Regards, <br>\
        #     Compfie Support Team''' % (
        #     group_name, legal_entity_name)
        self.send_email(
            receiver, subject, message, is_credential=True
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
                Dear %s,  Compliance %s has started.
                Due date for the compliance is %s
            ''' % (
                assignee_name, compliance_name, due_date
            )
        elif when == "Before Due Date":
            subject = "Task Reminder"
            message = '''
                Dear %s, Reminding you to Complete the compliance
                %s with due date %s
            ''' % (
                assignee_name, compliance_name, due_date
            )
        elif when == "After Due Date":
            subject = "Task Escalation"
            message = "Dear %s, Compliance %s is delayed" % (
                assignee_name, compliance_name, due_date
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
        self, receiver, le_name, group_name, expire_date
    ):
        subject = "Contract expiration reminder"

        message = ''' Your contract with Compfie for the legal entity %s of %s is about to expire on %s.
            Kindly renew your contract to avail the services continuously.
            ''' % (le_name, group_name, expire_date)

        cc_person = None
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "Email Failed for contract expiry ", message

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

    def notify_group_admin_toreassign_sp_compliances(
        self, service_provider_name, receiver, cc_person=[]
    ):
        subject = "Service Provider Compliance Reassign Notification"
        message = '''
            Dear Administrator, \
            Reassign %s user's compliances to someother user.
        ''' % (
               service_provider_name
        )
        try:
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e:
            print e
            print "", message
