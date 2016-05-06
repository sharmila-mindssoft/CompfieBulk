import MySQLdb as mysql
import datetime
import traceback

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (
    convert_to_dict, time_convertion,
    return_hour_minute
)

mysqlHost = KNOWLEDGE_DB_HOST
mysqlUser = KNOWLEDGE_DB_USERNAME
mysqlPassword = KNOWLEDGE_DB_PASSWORD
mysqlDatabase = KNOWLEDGE_DATABASE_NAME
mysqlPort = KNOWLEDGE_DB_PORT

NOTIFY_TIME = "00:00"  # 12 AM

email = EmailHandler()

def db_connection(host, user, password, db, port):
    connection = mysql.connect(
        host, user, password, db, port
    )
    connection.autocommit(False)
    return connection

def knowledge_db_connect():
    con = db_connection(mysqlHost, mysqlUser, mysqlPassword, mysqlDatabase, mysqlPort)
    return con

def get_countries():
    con = knowledge_db_connect()
    cursor = con.cursor()
    q = "SELECT country_id, country_name FROM tbl_countries"
    cursor.execute(q)
    rows = cursor.fetchall()
    cursor.close()
    return convert_to_dict(rows, ["country_id", "country_name"])

def get_client_db_list():
    print "begin fetching client info"
    con = knowledge_db_connect()
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
    print "Notification saved"
    cursor.close()
    save_notification_users(notification_id, assignee)
    if notify_to_all:
        if approval_person is not None :
            save_notification_users(notification_id, approval_person)
        if concurrence_person is not None or concurrence_person is not "NULL" :
            save_notification_users(notification_id, concurrence_person)


def get_inprogress_compliances(db, country_id):
    query = "SELECT distinct t1.compliance_history_id, t1.unit_id, t1.compliance_id, t1.start_date, \
        t1.due_date, t3.document_name, t3.compliance_task, \
        t2.assignee, t2.concurrence_person, t2.approval_person, t4.unit_code, t4.unit_name, \
        t4.business_group_id, t4.legal_entity_id, t4.division_id, t2.country_id, \
        t3.domain_id, t3.frequency_id FROM \
        tbl_compliance_history t1 INNER JOIN tbl_assigned_compliances t2 on \
        t1.compliance_id = t2.compliance_id \
        INNER JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id \
        INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id WHERE \
        IFNULL(t1.approve_status, 0) != 1 \
        AND t2.country_id = %s" % (country_id)
    # print query
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [
        "compliance_history_id", "unit_id", "compliance_id", "start_date", "due_date",
        "document_name", "compliance_task", "assignee", "concurrence_person", "approval_person",
        "unit_code", "unit_name", "business_group_id", "legal_entity_id", "division_id", "country_id",
        "domain_id", "frequency_id"
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
            for c in compliance_info:
                if c["due_date"] is None :
                    continue

                if c["due_date"].date() < current_date.date() :
                    continue
                days_left = abs((c["due_date"].date() - current_date.date()).days) + 1

                if c["document_name"] not in (None, "None", "") :
                    compliance_name = c["document_name"] + " - " + c["compliance_task"]
                else :
                    compliance_name = c["compliance_task"]
                date_diff = abs((current_date.date() - c["start_date"].date()).days)
                if date_diff == 0:
                    continue

                print date_diff
                print (date_diff % reminder_interval)

                notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
                extra_details = " %s - Reminder" % (c["compliance_history_id"])
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
    reminder_interval = int(client_info[0]["escalation_reminder_in_advance"])
    for c in compliance_info:
        if c["due_date"] is None :
            continue

        if c["document_name"] not in (None, "None", "") :
            compliance_name = c["document_name"] + " - " + c["compliance_task"]
        else :
            compliance_name = c["compliance_task"]

        if c["due_date"].date() < current_date.date() :
            continue

        if c["due_date"] is None :
            continue

        days_left = abs((c["due_date"].date() - current_date.date()).days) + 1
        if days_left == 0 :
            continue

        notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
        extra_details = " %s - Reminder" % (c["compliance_history_id"])
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
    for c in compliance_info :
        if c["due_date"] is None :
            continue

        if c["due_date"].date() > current_date.date() :
            continue

        if c["document_name"] not in (None, "None", "") :
            compliance_name = c["document_name"] + " - " + c["compliance_task"]
        else :
            compliance_name = c["compliance_task"]
        over_due_days = abs((current_date.date() - c["due_date"].date()).days) + 1
        if over_due_days == 0 :
            continue

        notification_text = "%s overdue by %s day(s)" % (compliance_name, over_due_days)
        extra_details = " %s - Escalation" % (c["compliance_history_id"])
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

def notify_task_details(db, client_id, country_id):
    client_info = get_client_settings(db)
    compliance_info = get_inprogress_compliances(db, country_id)
    if compliance_info :
        reminder_to_assignee(db, client_info, compliance_info)
        reminder_before_due_date(db, client_info, compliance_info)
        notify_escalation_to_all(db, client_info, compliance_info)

def run_notify_email_process(country_id):
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
                notify_task_details(db, client_id, country_id)
                db.commit()
            except Exception, e :
                print e
                db.rollback()
                print(traceback.format_exc())
    print "end email_notifications"
    print '--' * 20


def is_notify_time_reached(time_zone, country_id):
    # print time_zone
    # current_country_time = time_convertion(time_zone)
    # print "current_country_time"
    # print current_country_time
    # print type(current_country_time)
    now = return_hour_minute(time_convertion(time_zone))
    print now
    if now == NOTIFY_TIME :
        run_notify_email_process(country_id)
        pass

def run_email_process():
    country_time_zones = sorted(countries)
    country_list = get_countries()
    for c in country_list :
        name = c["country_name"]
        info = None
        for ct in country_time_zones :
            if name.lower() == ct.lower() :
                info = countries.get(ct)
                print info
                break
        if info :
            is_notify_time_reached(info.get("timezones")[0], c["country_id"])
