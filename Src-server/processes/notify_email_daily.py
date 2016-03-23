import MySQLdb as mysql
import datetime
import traceback

from smtplib import SMTP_SSL as SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

mysqlHost = "localhost"
mysqlUser = "root"
mysqlPassword = "123456"
mysqlDatabase = "compfie_knowledge"
mysqlPort = 3306

CLIENT_URL = "http://52.11.242.90:8082/"

class EmailNotification(object):
    def __init__(self):
        self.sender = "compfie.test@aparajitha.com"
        self.password = "Ctt@123"

    def send_email(self, receiver, subject, message, cc=None):
        server = SMTP("mail.aparajitha.com", 465)
        server.set_debuglevel(False)
        server.login(self.sender, self.password)

        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["To"] = receiver
        msg["subject"] = subject
        if cc is not None :
            if type(cc) is list :
                msg["Cc"] = ",".join(cc)
        msg.attach(MIMEText(message, "html"))
        response = server.sendmail(
            self.sender, receiver, msg.as_string()
        )
        server.close()

    def notify_to_assignee(
        self, assignee, days_left, compliance_name, unit_name,
        receiver
    ):
        subject = "Compliance Task Reminder"
        message = "Dear %s, \
            Only %s day(s) left to complete %s task for unit %s" % (
                assignee, days_left, compliance_name,
                unit_name
            )
        try :
            print
            self.send_email(receiver, subject, message)
            pass
        except Exception, e :
            print e
            print "Email Failed for notify to assignee %s ", message

    def notify_before_due_date(
        self, assignee, days_left, compliance_name, unit_name,
        receiver, cc_person
    ):
        subject = "Compliance Task Reminder"
        message = "Dear %s, \
            Only %s day(s) left to complete %s task for unit %s" % (
                assignee, days_left, compliance_name,
                unit_name
            )
        try :
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e :
            print e
            print "Email Failed for before due_date  ", message

    def notify_escalation(
        self, assignee, compliance_name, unit_name,
        over_due_days, receiver, cc_person
    ):
        subject = "Compliance Escalation Notification"
        message = "Dear %s, \
            Compliance %s for unit %s has overdue by %s day(s)." % (
                assignee, compliance_name, unit_name, over_due_days
            )
        try :
            self.send_email(receiver, subject, message, cc_person)
            pass
        except Exception, e :
            print e
            print "Email Failed for escalations", message

def convert_to_dict(data_list, columns) :
    assert type(data_list) in (list, tuple)
    if len(data_list) > 0:
        if type(data_list[0]) is tuple :
            result_list = []
            if len(data_list[0]) == len(columns) :
                for data in data_list:
                    result = {}
                    for i, d in enumerate(data):
                        result[columns[i]] = d
                    result_list.append(result)
            return result_list
        else :
            result = {}
            if len(data_list) == len(columns) :
                for i, d in enumerate(data_list):
                    result[columns[i]] = d
            return result
    else:
        return []


def db_connection(host, user, password, db, port):
    connection = mysql.connect(
        host, user, password, db, port
    )
    connection.autocommit(False)
    return connection


def get_client_db_list():
    print "begin fetching client info"
    con = db_connection(mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase, mysqlPort)
    cursor = con.cursor()
    query = "SELECT T1.client_id, T1.database_ip, T1.database_port, \
        T1.database_username, T1.database_password, T1.database_name \
        FROM tbl_client_database T1"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    if rows :
        columns = [
            "client_id", "database_ip", "database_port", "database_username",
            "database_password", "database_name"
        ]
        result = convert_to_dict(rows, columns)
        return result
    else :
        return None


def create_client_db_connection(data):
    if data is None :
        return None

    print "begin client db connection"
    client_connection = {}
    for d in data :
        try :
            db_conn = db_connection(
                d["database_ip"], d["database_username"],
                d["database_password"], d["database_name"],
                d["database_port"]
            )
        except Exception, e :
            print "unable to connect database %s", d
            print e
            continue
        client_connection[d["client_id"]] = db_conn

    return client_connection


def get_client_database():
    client_list = get_client_db_list()
    client_db = create_client_db_connection(client_list)
    return client_db

def get_current_date():
    date = datetime.datetime.today()
    return date

def get_current_month():
    month = get_current_date().month
    return month

def get_new_id(db, table_name, column_name):
    query = "SELECT MAX(%s)+1 FROM %s" % (column_name, table_name)
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    if row[0] is None :
        return 1
    return row[0]

def get_email_id_for_users(db, user_id):
    if user_id == 0 :
        q = "SELECT 'Administrator', username from tbl_admin where admin_id = %s" % (
            user_id
        )
        pass
    else :
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s" % (
            user_id
        )
    cursor = db.cursor()
    cursor.execute(q)
    row = cursor.fetchone()
    if row :
        return row[0], row[1]
    else :
        return None


def save_in_notification(
    db, country_id, domain_id, business_group_id, legal_entity_id, division_id,
    unit_id, compliance_id, assignee, concurrence_person, approval_person,
    notification_text, extra_details, notification_type_id, notify_to_all=True
):
    def save_notification_users(notification_id, user_id):
        if user_id is not "NULL" :
            q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
                VALUES (%s, %s)" % (notification_id, user_id)
            cur = db.cursor()
            cur.execute(q)
            cur.close()

    notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
    created_on = get_current_date()
    query = "INSERT INTO tbl_notifications_log \
        (notification_id, country_id, domain_id, business_group_id, \
        legal_entity_id, division_id, unit_id, compliance_id,\
        assignee, concurrence_person, approval_person, notification_type_id,\
        notification_text, extra_details, created_on\
        ) VALUES (%s, %s, %s, %s, %s, %s, \
        %s, %s, %s, %s, %s, %s, '%s', '%s', '%s')" % (
            notification_id, country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, compliance_id,
            assignee, concurrence_person, approval_person, notification_type_id,
            notification_text, extra_details, created_on
        )
    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    save_notification_users(notification_id, assignee)
    if notify_to_all:
        if approval_person is not None :
            save_notification_users(notification_id, approval_person)
        if concurrence_person is not None or concurrence_person is not "NULL" :
            save_notification_users(notification_id, concurrence_person)


def get_inprogress_compliances(db):
    query = "SELECT t1.compliance_history_id, t1.unit_id, t1.compliance_id, t1.start_date, \
        t1.due_date, t3.document_name, t3.compliance_task, \
        t2.assignee, t2.concurrence_person, t2.approval_person, t4.unit_code, t4.unit_name, \
        t4.business_group_id, t4.legal_entity_id, t4.division_id, t2.country_id, \
        t3.domain_id FROM \
        tbl_compliance_history t1 INNER JOIN tbl_assigned_compliances t2 on \
        t1.compliance_id = t2.compliance_id \
        INNER JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id \
        INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id WHERE \
        IFNULL(t1.approve_status, 0) != 1"
    # print query
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [
        "compliance_history_id", "unit_id", "compliance_id", "start_date", "due_date",
        "document_name", "compliance_task", "assignee", "concurrence_person", "approval_person",
        "unit_code", "unit_name", "business_group_id", "legal_entity_id", "division_id", "country_id",
        "domain_id"
    ]
    result = convert_to_dict(rows, columns)
    print '*' * 10
    # print result
    print '*' * 10

    return result

def get_client_settings(db):
    query = "SELECT assignee_reminder, escalation_reminder_in_advance, escalation_reminder \
        FROM tbl_client_groups"
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = ["assignee_reminder", "escalation_reminder_in_advance", "escalation_reminder"]
    result = convert_to_dict(rows, columns)
    return result

def reminder_to_assignee(db, client_info, compliance_info):
    current_date = get_current_date()
    try :
        print "begin process to remind inprogress compliance task %s " % (current_date)
        # client_info = get_client_settings(db)
        if client_info :
            reminder_interval = int(client_info[0]["assignee_reminder"])
            # compliance_info = get_inprogress_compliances(db)
            count = 0
            email = EmailNotification()
            for c in compliance_info:
                if c["document_name"] not in (None, "None", "") :
                    compliance_name = c["document_name"] + " - " + c["compliance_task"]
                else :
                    compliance_name = c["compliance_task"]
                date_diff = (current_date - c["start_date"]).days
                if c["due_date"] is None :
                    continue
                days_left = (c["due_date"] - current_date).days + 1
                if days_left <= 0 :
                    continue
                notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
                extra_details = ""
                if (date_diff % reminder_interval) == 0 :
                    save_in_notification(
                        db, c["country_id"], c["domain_id"], c["business_group_id"], c["legal_entity_id"],
                        c["division_id"], c["unit_id"], c["compliance_id"], c["assignee"],
                        c["concurrence_person"], c["approval_person"],
                        notification_text, extra_details, notification_type_id=2, notify_to_all=False
                    )
                    a_name, assignee_email = get_email_id_for_users(db, c["assignee"])
                    email.notify_to_assignee(
                        a_name, days_left, compliance_name,
                        c["unit_name"], assignee_email
                    )
                    count += 1
            print "%s compliances remindered" % (count)
    except Exception, e:
        print e
        print(traceback.format_exc())

def reminder_before_due_date(db, client_info, compliance_info):
    current_date = get_current_date()
    print "begin process to remind inprogress compliance task to all %s " % (current_date)
    # client_info = get_client_settings(db)
    email = EmailNotification()
    reminder_interval = int(client_info[0]["escalation_reminder_in_advance"])
    for c in compliance_info:
        if c["document_name"] not in (None, "None", "") :
            compliance_name = c["document_name"] + " - " + c["compliance_task"]
        else :
            compliance_name = c["compliance_task"]
        if c["due_date"] is None :
            continue

        days_left = (c["due_date"] - current_date).days + 1
        if days_left <= 0 :
            continue
        notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
        extra_details = ""
        if days_left == reminder_interval:
            save_in_notification(
                db, c["country_id"], c["domain_id"], c["business_group_id"],
                c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                extra_details, notification_type_id=2
            )
            a_name, assignee_email = get_email_id_for_users(db, c["assignee"])
            cc_person = []
            concurrence_person = c["concurrence_person"]
            if concurrence_person == 0 :
                concurrence_person = None
            if concurrence_person is not None :
                c_name, concurrence_email = get_email_id_for_users(db, concurrence_person)
                cc_person.append(concurrence_email)
            ap_name, approval_email = get_email_id_for_users(db, c["approval_person"])
            cc_person.append(approval_email)
            email.notify_before_due_date(
                a_name, days_left, compliance_name,
                c["unit_name"],
                assignee_email, cc_person
            )

def notify_escalation_to_all(db, client_info, compliance_info):
    current_date = get_current_date()
    print "begin process to notify escalations to all %s" % (current_date)
    escalation_interval = int(client_info[0]["escalation_reminder"])
    email = EmailNotification()
    for c in compliance_info :
        if c["document_name"] not in (None, "None", "") :
            compliance_name = c["document_name"] + " - " + c["compliance_task"]
        else :
            compliance_name = c["compliance_task"]
        over_due_days = (current_date - c["due_date"]).days + 1
        if over_due_days <= 0 :
            continue
        notification_text = "%s overdue by %s day(s)" % (compliance_name, over_due_days)
        extra_details = ""
        if (over_due_days % escalation_interval) == 0 :
            save_in_notification(
                db, c["country_id"], c["domain_id"], c["business_group_id"],
                c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                extra_details, notification_type_id=3
            )
            a_name, assignee_email = get_email_id_for_users(db, c["assignee"])
            cc_person = []
            concurrence_person = c["concurrence_person"]
            if concurrence_person == 0 :
                concurrence_person = None
            if concurrence_person is not None :
                c_name, concurrence_email = get_email_id_for_users(db, concurrence_person)
                cc_person.append(concurrence_email)
            ap_name, approval_email = get_email_id_for_users(db, c["approval_person"])
            cc_person.append(approval_email)
            email.notify_before_due_date(
                a_name, over_due_days, compliance_name,
                c["unit_name"],
                assignee_email, cc_person
            )

def notify_task_details(db, client_id):
    client_info = get_client_settings(db)
    compliance_info = get_inprogress_compliances(db)
    if compliance_info :
        reminder_to_assignee(db, client_info, compliance_info)
        reminder_before_due_date(db, client_info, compliance_info)
        notify_escalation_to_all(db, client_info, compliance_info)

def notify_before_contract_period(db, client_id):
    query = "SELECT contract_to, group_name FROM tbl_client_groups"
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    contract_to_str = str(rows[0][0])
    group_name = str(rows[0][1])
    contract_to_parts = [int(x) for x in contract_to_str.split("-")]
    contract_to = datetime.date(
        contract_to_parts[0], contract_to_parts[1], contract_to_parts[2]
    )
    delta = contract_to - datetime.datetime.now().date()
    if delta.days <= 30:
        notification_text = "Your contract with Compfie will expire in %d \
        days. Kindly renew your contract to avail the services continuosuly" % (
            delta.days
        )
        extra_details = "Reminder : Contract Expiration"

        notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
        created_on = datetime.datetime.now()
        query = "INSERT INTO tbl_notifications_log \
            (notification_id, notification_type_id,\
            notification_text, extra_details, created_on\
            ) VALUES (%s, %s, '%s', '%s', '%s')" % (
                notification_id, 2,
                notification_text, extra_details, created_on
            )
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()

        q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
            VALUES (%s, %s)" % (notification_id, 0)
        cur = db.cursor()
        cur.execute(q)
        cur.close()
        print '*' * 10
        print "contract period expire notification sent ot %s" % (group_name)
        print '*' * 10

def main():
    print '--' * 20
    print "begin email_notification"
    print "current_date datetime ", datetime.datetime.now()
    client_info = get_client_database()
    if client_info is not None :
        for client_id, db in client_info.iteritems() :
            print "~~~~~~~~~~~"
            print client_id
            try :
                db.commit()
                notify_task_details(db, client_id)
                # notify_before_contract_period(db, client_id)
                db.commit()
            except Exception, e :
                print e
                db.rollback()
                print(traceback.format_exc())
    print "end email_notifications"
    print '--' * 20

if __name__ == "__main__" :
    main()
