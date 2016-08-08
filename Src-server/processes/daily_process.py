#!/usr/bin/python

import os
import datetime
import json
import traceback
import threading
import MySQLdb as mysql
from datetime import timedelta

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (
    convert_to_dict, time_convertion, return_date,
    addMonth, addDays, addYears,
    create_new_date, convert_string_to_date,
    insert
)

mysqlHost = KNOWLEDGE_DB_HOST
mysqlUser = KNOWLEDGE_DB_USERNAME
mysqlPassword = KNOWLEDGE_DB_PASSWORD
mysqlDatabase = KNOWLEDGE_DATABASE_NAME
mysqlPort = KNOWLEDGE_DB_PORT

expired_download_path = "/expired/download/"
expired_folder_path = "./expired/"

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
    # print "begin fetching client info"
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

    # print "begin client db connection"
    client_connection = {}
    for d in data :
        try :
            db_conn = db_connection(
                d["database_ip"], d["database_username"],
                d["database_password"], d["database_name"],
                d["database_port"]
            )
            client_connection[d["client_id"]] = db_conn
        except Exception:
            # print "unable to connect database %s", d
            # print e
            continue

    return client_connection

def get_client_database():
    client_list = get_client_db_list()
    client_db = create_client_db_connection(client_list)
    return client_db

def get_contract_expiring_clients():
    con = knowledge_db_connect()
    cursor = con.cursor()
    query = "SELECT client_id FROM tbl_client_groups \
    WHERE DATEDIFF(contract_to, now()) < 30 and contract_to > now();"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    client_ids = []
    for row in rows:
        client_ids.append(row[0])
    return client_ids

def get_compliance_to_start(db, client_id, current_date, country_id):
    query = "SELECT t1.country_id, t1.unit_id, t1.compliance_id, t1.statutory_dates, \
        t1.trigger_before_days, t1.due_date, t1.validity_date,\
        t2.document_name, t2.compliance_task, t2.frequency_id, t2.repeats_type_id,\
        t2.repeats_every, (t1.due_date - INTERVAL t1.trigger_before_days DAY) start_date,\
        t3.unit_id, t3.unit_code, t3.unit_name, t3.business_group_id,\
        t3.legal_entity_id, t3.division_id, t2.domain_id, \
        t1.assignee, t1.concurrence_person, t1.approval_person, \
        t4.compliance_id \
        from tbl_assigned_compliances t1\
        INNER JOIN tbl_units t3 on t1.unit_id = t3.unit_id\
        INNER JOIN tbl_compliances t2 on t1.compliance_id = t2.compliance_id\
        LEFT JOIN tbl_compliance_history t4 ON (t4.unit_id = t1.unit_id \
            AND t4.compliance_id = t1.compliance_id AND t2.frequency_id = 1)\
        WHERE (t1.due_date - INTERVAL t1.trigger_before_days DAY) <= '%s' \
        AND t1.is_active = 1 AND t2.is_active = 1 \
        AND t1.country_id = %s \
        AND t4.compliance_id is null " % (current_date, country_id)

    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date", "document_name", "compliance_task",
        "frequency", "repeat_type_id", "repeats_every", "start_date",
        "unit_id", "unit_code", "unit_name",
        "business_group_id", "legal_entity_id", "division_id",
        "domain_id",
        "assignee", "concurrence_person", "approval_person", "t4_compliance_id"
    ]
    result = convert_to_dict(rows, columns)

    return result

def get_email_id_for_users(db, user_id):
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

def calculate_next_due_date(
    frequency, statutory_dates, repeat_type,
    repeat_every, old_due_date
):
    # frequency 1: One Time, 2 : Periodical, 3 : Review, 4: On occurance
    #  repeat_type 1 : Days, 2 : Months, 3 : years
    repeat_every = int(repeat_every)
    repeat_type = int(repeat_type)
    statutory_dates = json.loads(statutory_dates)
    trigger_before_days = None
    if statutory_dates == []:
        statutory_dates = None
    if frequency == 2 or frequency == 3 :
        if statutory_dates is None or len(statutory_dates) == 1 :
            if repeat_type == 1 :
                new_due_date = addDays(repeat_every, old_due_date)
            elif repeat_type == 2 :
                new_due_date = addMonth(repeat_every, old_due_date)
            elif repeat_type == 3 :
                new_due_date = addYears(repeat_every, old_due_date)
            else :
                "repeat_type not matched"
                new_due_date = old_due_date
            return (new_due_date,  trigger_before_days)
        else :
            temp_date = convert_string_to_date(str(old_due_date))
            old_month = temp_date.month
            if repeat_type == 2 :
                for index, dat in enumerate(statutory_dates) :
                    day = dat["statutory_date"]
                    month = dat["statutory_month"]
                    if month is not None and month == old_month :
                        if index == len(statutory_dates)-1 :
                            day = statutory_dates[0]["statutory_date"]
                            month = statutory_dates[0]["statutory_month"]
                            trigger_before_days = statutory_dates[0]["trigger_before_days"]
                            new_due_date = create_new_date(old_due_date, day, month)
                            break
                        else :
                            day = statutory_dates[index + 1]["statutory_date"]
                            month = statutory_dates[index + 1]["statutory_month"]
                            trigger_before_days = statutory_dates[index + 1]["trigger_before_days"]
                            new_due_date = create_new_date(old_due_date, day, month)
                            break
                    else :
                        if (month > old_month) :
                            day = dat["statutory_date"]
                            month = dat["statutory_month"]
                            trigger_before_days = dat["trigger_before_days"]
                            new_due_date = create_new_date(old_due_date, day, month)
                            break
                        else :
                            if index == len(statutory_dates)-1 :
                                day = statutory_dates[0]["statutory_date"]
                                month = statutory_dates[0]["statutory_month"]
                                trigger_before_days = dat["trigger_before_days"]
                                new_due_date = create_new_date(old_due_date, day, month)
                                break

                return (new_due_date, trigger_before_days)
    else :
        return old_due_date, trigger_before_days

def get_new_id(db, table_name, column_name):
    query = "SELECT MAX(%s)+1 FROM %s" % (column_name, table_name)
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    if row[0] is None :
        return 1
    return row[0]

def save_in_compliance_history(
    db, unit_id, compliance_id, start_date, due_date, next_due_date,
    assignee, concurrence, approve
):
    compliance_history_id = get_new_id(db, "tbl_compliance_history", "compliance_history_id")
    if concurrence is not None:
        columns = "compliance_history_id, unit_id, compliance_id, \
                start_date, due_date, next_due_date, completed_by, approved_by, concurred_by"
        values = (
            columns, compliance_history_id, unit_id, compliance_id,
            start_date, due_date, next_due_date, assignee,  approve, concurrence
        )
        query = "INSERT INTO tbl_compliance_history (%s) \
            VALUES (%s, %s, %s, '%s', '%s', '%s', %s, %s, %s) " % values

    else :
        columns = "compliance_history_id, unit_id, compliance_id, \
                start_date, due_date, next_due_date, completed_by, approved_by"
        values = (
            columns, compliance_history_id, unit_id, compliance_id,
            start_date, due_date, next_due_date, assignee,  approve
        )

        query = "INSERT INTO tbl_compliance_history (%s) \
            VALUES (%s, %s, %s, '%s', '%s', '%s', %s, %s) " % values

    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    return compliance_history_id

def update_assign_compliance_due_date(db, trigger_before, due_date, unit_id, compliance_id):
    query = "UPDATE tbl_assigned_compliances set due_date='%s', trigger_before_days=%s \
        WHERE unit_id = %s AND compliance_id = %s \
        " % (due_date, trigger_before, unit_id, compliance_id)
    # print query
    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()

def save_in_notification(
    db, country_id, domain_id, business_group_id, legal_entity_id, division_id,
    unit_id, compliance_id, assignee, concurrence_person, approval_person,
    notification_text, extra_details, notification_type_id, notify_to_all=True
):
    def save_notification_users(notification_id, user_id):
        if user_id is not "NULL" and user_id is not None  :
            q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
                VALUES (%s, %s)" % (notification_id, user_id)
            cur = db.cursor()
            cur.execute(q)
            cur.close()

    notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
    created_on = datetime.datetime.now()
    column = [
            "notification_id", "country_id", "domain_id",
            "legal_entity_id", "unit_id", "compliance_id",
            "assignee", "approval_person", "notification_type_id",
            "notification_text", "extra_details", "created_on"
        ]
    values = [
        notification_id, country_id, domain_id,
        legal_entity_id, unit_id, compliance_id,
        assignee, approval_person, notification_type_id,
        notification_text, extra_details, created_on
    ]
    if business_group_id is not None :
        column.append("business_group_id")
        values.append(business_group_id)
    if division_id is not None :
        column.append("division_id")
        values.append(division_id)
    if concurrence_person is not None :
        column.append("concurrence_person")
        values.append(concurrence_person)

    query = insert("tbl_notifications_log", column, values)

    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    save_notification_users(notification_id, assignee)
    if notify_to_all:
        if approval_person is not None and assignee != approval_person:
            save_notification_users(notification_id, approval_person)
        if concurrence_person is not None or concurrence_person is not "NULL" :
            save_notification_users(notification_id, concurrence_person)

def start_new_task(db, client_id, current_date, country_id):
    def notify(d, due_date, next_due_date, approval_person):
        compliance_history_id = save_in_compliance_history(
            db, int(d["unit_id"]), int(d["compliance_id"]), current_date,
            due_date, next_due_date, int(d["assignee"]),
            d["concurrence_person"], int(approval_person)
        )

        if d["document_name"] :
            compliance_name = d["document_name"] + " - " + d["compliance_task"]
        else :
            compliance_name = d["compliance_task"]
        unit_name = d["unit_code"] + " - " + d["unit_name"]
        notification_text = "Compliance task %s started" % (compliance_name)
        extra_details = " %s - Compliance Started" % (compliance_history_id)
        notification_type_id = 1   # 1 = notification
        save_in_notification(
            db, d["country_id"], d["domain_id"], d["business_group_id"], d["legal_entity_id"],
            d["division_id"], d["unit_id"], d["compliance_id"], d["assignee"],
            d["concurrence_person"], d["approval_person"],
            notification_text, extra_details, notification_type_id
        )
        a_name, assignee_email = get_email_id_for_users(db, d["assignee"])
        notify_new_task = threading.Thread(
            target=email.notify_compliance_start,
            args=[
                a_name, compliance_name, unit_name,
                d["due_date"], assignee_email
            ]
        )
        notify_new_task.start()

    def start_next_due_date_task(d, due_date, approval_person) :
        next_due_date, trigger_before = calculate_next_due_date(
            d["frequency"], d["statutory_dates"], d["repeat_type_id"],
            d["repeats_every"], due_date
        )

        if trigger_before is None:
            trigger_before = int(d["trigger_before_days"])

        notify(d, due_date, next_due_date, approval_person)
        return next_due_date, trigger_before

    data = get_compliance_to_start(db, client_id, current_date, country_id)
    count = 0
    for d in data :
        try :
            approval_person = int(d["approval_person"])
            if d["frequency"] == 1 :
                next_due_date = "0000-00-00"
                notify(d, d["due_date"], next_due_date, approval_person)
            else:
                next_due_date = trigger_before = None
                due_date = d["due_date"]
                next_due_date, trigger_before = start_next_due_date_task(d, due_date, approval_person)
                update_assign_compliance_due_date(db, trigger_before, next_due_date, d["unit_id"], d["compliance_id"])
                if next_due_date is not None :
                    while (next_due_date - timedelta(days=trigger_before)) <= current_date :
                        # start for next-due-date
                        next_due_date, trigger_before = start_next_due_date_task(d, next_due_date, approval_person)
                        update_assign_compliance_due_date(db, trigger_before, next_due_date, d["unit_id"], d["compliance_id"])

            count += 1
        except Exception, e :
            print e
            continue
            # print(traceback.format_exc())

    print " %s compliances started for client_id %s - %s" % (count, client_id, current_date)

def notify_before_contract_period(db, client_id):
    cursor = db.cursor()

    # download_link = exp(client_id, db).generate_report()

    query = "SELECT group_name FROM tbl_client_groups"
    cursor.execute(query)
    rows = cursor.fetchall()
    group_name = rows[0][0]

    notification_text = '''Your contract with Compfie for the group \"%s\" is about to expire. \
    Kindly renew your contract to avail the services continuously.'''  % group_name
    # Before contract expiration \
    # You can download documents of %s <a href="%s">here </a> ''' % (
    #     group_name, download_link
    # )
    extra_details = "0 - Reminder : Contract Expiration"

    notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
    created_on = datetime.datetime.now()
    query = "INSERT INTO tbl_notifications_log \
        (notification_id, notification_type_id,\
        notification_text, extra_details, created_on\
        ) VALUES (%s, %s, '%s', '%s', '%s')" % (
            notification_id, 2,
            notification_text, extra_details, created_on
        )
    cursor.execute(query)
    cursor.close()

    q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
        VALUES (%s, %s)" % (notification_id, 0)
    cur = db.cursor()
    cur.execute(q)

    q = "SELECT email_id from tbl_users where is_active = 1 and is_primary_admin = 1 "
    cur.execute(q)
    rows = cur.fetchall()
    admin_mail_id = rows[0][0]
    cur.close()
    email.notify_contract_expiration(
        admin_mail_id, notification_text
    )

def check_service_provider_contract_period(
    db, client_id
):
    query = "UPDATE tbl_service_providers set is_active = 0 WHERE \
    now() not between contract_from and contract_to"
    cursor = db.cursor()
    cursor.execute(query)

def is_already_notified(
    client_id
):
    client_folder_path = "%s%s" % (expired_folder_path, str(client_id))
    return os.path.isdir(client_folder_path)


def run_daily_process(country_id, current_date):
    client_info = get_client_database()
    # client_ids = get_contract_expiring_clients()
    if client_info is not None :
        for client_id, db in client_info.iteritems() :
            try :
                start_new_task(db, client_id, current_date, country_id)
                db.commit()
                check_service_provider_contract_period(db, client_id)
                # if client_id in client_ids and not is_already_notified(client_id):
                #     notify_before_contract_period(db, client_id)
                db.commit()
            except Exception, e :
                print e
                db.rollback()
                # print(traceback.format_exc())

def run_daily_process_country_wise():
    country_time_zones = sorted(countries)
    country_list = get_countries()
    for c in country_list :
        name = c["country_name"].replace(" ", "")
        name = name.replace("_", "")
        name = name.replace("-", "")
        info = None
        for ct in country_time_zones :
            ct = ct.replace(" ", "")
            if name.lower() == ct.lower() :
                info = countries.get(ct)
                # print info
                break
        if info :
            current_date = return_date(time_convertion(info.get("timezones")[0]))
            # print "country -- ", c["country_name"]
            # print
            run_daily_process(c["country_id"], current_date)
