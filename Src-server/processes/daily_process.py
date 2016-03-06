#!/usr/bin/python

# run every 5 mins
# PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin
# */5 * * * * ~/Python/workspace/Compliance-Mirror/Src-server/processes/daily_process.py >> ~/Python/workspace/Compliance-Mirror/Src-server/processes/daily_process.log 2>&1

# sudo chmod 777 daily_process.py

# client db details from server
# loop every client
# ## Task start
# check current date with due date, then start task
# insert record in history table
# update assigned compliance (due_date)
# insert record in notification
# Email to assignee, concurrance

# ##  Before due_date (from settings)
# save notification
# send mail (assignee, concurrence, approve)

# ## After due_date till get approve
# save notifocation
# send mail (assignee, concurrence, approve)

# ## before contract period expiration
# Validate datetime based on country

import MySQLdb as mysql
import datetime
import json
import traceback

mysqlHost = "localhost"
mysqlUser = "root"
mysqlPassword = "123456"
mysqlDatabase = "mirror_knowledge"
mysqlPort = 3306


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
        db_conn = db_connection(
            d["database_ip"], d["database_username"],
            d["database_password"], d["database_name"],
            d["database_port"]
        )
        client_connection[d["client_id"]] = db_conn

    return client_connection


def get_client_database():
    client_list = get_client_db_list()
    client_db = create_client_db_connection(client_list)
    return client_db

def get_current_date():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    return date

def get_current_month():
    month = datetime.datetime.now().month
    return month

def get_country_wise_timestamp():
    pass
    #  yyyy-mm-dd

def get_compliance_to_start(db, client_id, current_date):
    print "fetching task details to start compliance for client id - %s, %s" % (client_id, current_date)
    query = "SELECT t1.country_id, t1.unit_id, t1.compliance_id, \
        t1.statutory_dates, t1.trigger_before_days, t1.due_date, t1.validity_date, \
        (select group_concat(document_name, '-', compliance_task) from tbl_compliances where compliance_id = t1.compliance_id) compliance_name, \
        (select frequency_id from tbl_compliances WHERE compliance_id = t1.compliance_id)frequency, \
        (select repeats_type_id from tbl_compliances WHERE compliance_id = t1.compliance_id) repeat_type_id, \
        (select repeats_every from tbl_compliances WHERE compliance_id = t1.compliance_id) repeats_every, \
        (t1.due_date - INTERVAL t1.trigger_before_days DAY) start_date, \
        (select business_group_id from tbl_units where unit_id = t1.unit_id) business_group_id, \
        (select legal_entity_id from tbl_units where unit_id = t1.unit_id) legal_entity_id, \
        (select division_id from tbl_units where unit_id = t1.unit_id) division_id, \
        (select distinct a.domain_id from tbl_client_statutories a \
            INNER JOIN tbl_client_compliances b ON a.client_statutory_id = b.client_statutory_id\
            INNER JOIN tbl_compliances c ON c.compliance_id = b.compliance_id \
            WHERE c.compliance_id = t1.compliance_id AND a.unit_id = t1.unit_id \
            AND a.country_id = t1.country_id) domain_id,\
        t1.assignee, t1.concurrence_person, t1.approval_person\
        FROM tbl_assigned_compliances t1 \
        WHERE \
        (select frequency_id from tbl_compliances WHERE compliance_id = t1.compliance_id) not in (4) \
        AND \
        (t1.due_date - INTERVAL t1.trigger_before_days DAY) <=  '%s'" % (current_date)

    # print query
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [
        "country_id", "unit_id", "compliance_id", "statutory_dates",
        "trigger_before_days", "due_date", "validity_date", "compliance_name",
        "frequency", "repeat_type_id", "repeats_every", "start_date",
        "business_group_id", "legal_entity_id", "division_id", "domain_id",
        "assignee", "concurrence_person", "approval_person"
    ]
    result = convert_to_dict(rows, columns)
    print '*' * 10
    print result
    print '*' * 10

    return result

def addMonth(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value*366 / 12))
    return new_date

def addDays(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value))
    return new_date

def addYears(value, due_date):
    new_date = (due_date + datetime.timedelta(days=value * 366))
    return new_date

def convert_string_to_date(due_date):
    due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    return due_date

def create_new_date(date, days, month):
    current_date = date
    try :
        date = date.replace(day=int(days), month=int(month))
    except ValueError :
        if date.month == 12 :
            days = 31
        else :
            days = (date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)).day
        date = date.replace(day=days)

    if date < current_date :
        date = date.replace(year=date.year+1)
    return date

def calculate_next_due_date(
    frequency, statutory_dates, repeat_type,
    repeat_every, old_due_date
):
    # frequency 1: One Time, 2 : Periodical, 3 : Review, 4: On occurance
    #  repeat_type 1 : Days, 2 : Months, 3 : years
    repeat_every = int(repeat_every)
    repeat_type = int(repeat_type)
    # current_month = get_current_month()
    # current_date = convert_string_to_date(get_current_date())
    statutory_dates = json.loads(statutory_dates)
    trigger_before_days = None
    print
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
            return (new_due_date,  trigger_before_days)
        else :
            print "due_date from next_due_date"
            temp_date = convert_string_to_date(old_due_date)
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
                            print "first index"
                            new_due_date = create_new_date(old_due_date, day, month)
                            break
                        else :
                            day = statutory_dates[index + 1]["statutory_date"]
                            month = statutory_dates[index + 1]["statutory_month"]
                            trigger_before_days = statutory_dates[index + 1]["trigger_before_days"]
                            print "next index"
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
                                print "first index"
                                trigger_before_days = dat["trigger_before_days"]
                                new_due_date = create_new_date(old_due_date, day, month)
                                break

                return (new_due_date, trigger_before_days)
    else :
        return old_due_date

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
    db, unit_id, compliance_id, start_date, due_date, next_due_date, assignee, concurrence, approve
):
    print "new task saved in history (unit_id, compliance_id, start_date) %s, %s, %s" % (unit_id, compliance_id, start_date)
    compliance_history_id = get_new_id(db, "tbl_compliance_history", "compliance_history_id")
    query = "INSERT INTO tbl_compliance_history (compliance_history_id, unit_id, compliance_id, \
            start_date, due_date, next_due_date, completed_by, concurred_by, approved_by) \
        VALUES (%s, %s, %s, '%s', '%s', '%s', %s, %s, %s) " % (
                compliance_history_id, unit_id, compliance_id,
                start_date, due_date, next_due_date, assignee, concurrence, approve
            )
    # print
    # print query
    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()

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
        q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
            VALUES (%s, %s)" % (notification_id, user_id)
        cur = db.cursor()
        cur.execute(q)
        cur.close()

    notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
    created_on = datetime.datetime.now()
    query = "INSERT INTO tbl_notifications_log \
        (notification_id, country_id, domain_id, business_group_id, \
        legal_entity_id, division_id, unit_id, compliance_id,\
        assignee, concurrence_person, approval_person, notification_type_id,\
        notification_text, extra_details, updated_on\
        ) VALUES (%s, %s, %s, %s, %s, %s, \
        %s, %s, %s, %s, %s, %s, '%s', '%s', '%s')" % (
            notification_id, country_id, domain_id, business_group_id,
            legal_entity_id, division_id, unit_id, compliance_id,
            assignee, concurrence_person, approval_person, notification_type_id,
            notification_text, extra_details, created_on
        )
    # print query
    # print
    cursor = db.cursor()
    cursor.execute(query)
    cursor.close()
    save_notification_users(notification_id, assignee)
    if notify_to_all:
        if approval_person is not None :
            save_notification_users(notification_id, approval_person)
        if concurrence_person is not None or concurrence_person is not "NULL" :
            save_notification_users(notification_id, concurrence_person)

def start_new_task(db, client_id, current_date):
    print current_date
    print "begin process to start new task  - %s" % (current_date)
    data = get_compliance_to_start(db, client_id, current_date)
    count = 0
    for d in data :
        if d["division_id"] == 0 :
            d["division_id"] = "NULL"
        if d["concurrence_person"] == 0 :
            d["concurrence_person"] = "NULL"
        approval_person = d["approval_person"]
        if d["frequency"] == 1 :
            next_due_date = ""
            save_in_compliance_history(
                db, int(d["unit_id"]), int(d["compliance_id"]), current_date,
                d["due_date"], next_due_date, int(d["assignee"], d["concurrence_person"], int(approval_person))
            )
        else:
            next_due_date, trigger_before = calculate_next_due_date(
                d["frequency"], d["statutory_dates"], d["repeat_type_id"],
                d["repeats_every"], d["due_date"]
            )
            save_in_compliance_history(
                db, int(d["unit_id"]), int(d["compliance_id"]), current_date,
                d["due_date"], next_due_date, int(d["assignee"], d["concurrence_person"], int(approval_person))
            )
            if trigger_before is None:
                trigger_before = d["trigger_before_days"]
            update_assign_compliance_due_date(db, trigger_before, next_due_date, d["unit_id"], d["compliance_id"])
            notification_text = "Compliance task %s started" % (d["compliance_name"])
            extra_details = "Compliance Started"
            notification_type_id = 1   # 1 = notification
            save_in_notification(
                db, d["country_id"], d["domain_id"], d["business_group_id"], d["legal_entity_id"],
                d["division_id"], d["unit_id"], d["compliance_id"], d["assignee"],
                d["concurrence_person"], d["approval_person"],
                notification_text, extra_details, notification_type_id
            )
        count += 1

    print " %s compliances started for - %s" % (count, current_date)

def get_inprogress_compliances(db):
    query = "SELECT t1.compliance_history_id, t1.unit_id, t1.compliance_id, t1.start_date, t1.due_date, \
        (select group_concat(document_name, '-', compliance_task) from tbl_compliances where compliance_id = t1.compliance_id) compliance_name, \
        (select assignee from tbl_assigned_compliances \
            where unit_id = t1.unit_id and compliance_id = t1.compliance_id) assignee, \
        (select concurrence_person from tbl_assigned_compliances \
            where unit_id = t1.unit_id and compliance_id = t1.compliance_id) concurrence_person, \
        (select concurrence_person from tbl_assigned_compliances \
            where unit_id = t1.unit_id and compliance_id = t1.compliance_id) approval_person, \
        (select business_group_id from tbl_units where unit_id = t1.unit_id) business_group_id, \
        (select legal_entity_id from tbl_units where unit_id = t1.unit_id) legal_entity_id, \
        (select division_id from tbl_units where unit_id = t1.unit_id) division_id, \
        (select country_id from tbl_units where unit_id = t1.unit_id) country_id, \
        (select distinct a.domain_id from tbl_client_statutories a \
            INNER JOIN tbl_client_compliances b ON a.client_statutory_id = b.client_statutory_id\
            INNER JOIN tbl_compliances c ON c.compliance_id = b.compliance_id \
            WHERE c.compliance_id = t1.compliance_id AND a.unit_id = t1.unit_id \
        ) domain_id \
        FROM tbl_compliance_history t1 WHERE approve_status = NULL OR approve_status != 1  "
    # print query
    cursor = db.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [
        "compliance_history_id", "unit_id", "compliance_id", "start_date", "due_date",
        "compliance_name", "assignee", "concurrence_person", "approval_person",
        "business_group_id", "legal_entity_id", "division_id", "country_id",
        "domain_id"
    ]
    result = convert_to_dict(rows, columns)
    print '*' * 10
    print result
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
        print client_info
        if client_info :
            reminder_interval = int(client_info["assignee_reminder"])
            # compliance_info = get_inprogress_compliances(db)
            count = 0
            for c in compliance_info:
                date_diff = (current_date - c["start_date"]).days
                days_left = (c["due_date"] - current_date).days
                notification_text = "%s days left to complete %s task" % (days_left, c["compliance_name"])
                extra_details = ""
                if (date_diff % reminder_interval) == 0 :
                    save_in_notification(
                        db, c["country_id"], c["domain_id"], c["business_group_id"], c["legal_entity_id"],
                        c["division_id"], c["unit_id"], c["compliance_id"], c["assignee"],
                        c["concurrence_person"], c["approval_person"],
                        notification_text, extra_details, notification_type_id=2, notify_to_all=False
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
    reminder_interval = int(client_info["escalation_reminder_in_advance"])
    for c in compliance_info:
        days_left = (c["due_date"] - current_date).days
        notification_text = "%s days left to complete %s task" % (days_left, c["compliance_name"])
        extra_details = ""
        if days_left == reminder_interval:
            save_in_notification(
                db, c["country_id"], c["domain_id"], c["business_group_id"],
                c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                extra_details, notification_type_id=2
            )

def notify_escalation_to_all(db, client_info, compliance_info):
    current_date = get_current_date()
    print "begin process to notify escalations to all %s" % (current_date)
    escalation_interval = int(client_info["escalation_reminder"])
    for c in compliance_info :
        over_due_days = (current_date - c["due_date"]).days
        notification_text = "%s over-due by %s days" % (c["compliance_name"], over_due_days)
        extra_details = ""
        if (over_due_days % escalation_interval) == 0 :
            save_in_notification(
                db, c["country_id"], c["domain_id"], c["business_group_id"],
                c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                extra_details, notification_type_id=3
            )

def notify_task_details(db, client_id):
    client_info = get_client_settings(db)
    compliance_info = get_inprogress_compliances(db)
    if compliance_info :
        reminder_to_assignee(db, client_info, compliance_info)
        reminder_before_due_date(db, client_info, compliance_info)
        notify_escalation_to_all(db, client_info, compliance_info)

def notify_before_contract_period(db, client_id):
    pass

def main():
    print '*' * 20
    current_date = get_current_date()
    print "current_date datetime ", current_date
    client_info = get_client_database()
    try :
        for client_id, db in client_info.iteritems() :
            start_new_task(db, client_id, current_date)
            db.commit()
            notify_task_details(db, client_id)
            db.commit()
    except Exception, e :
        print e
        db.rollback()

    print '*' * 20

if __name__ == "__main__" :
    main()
