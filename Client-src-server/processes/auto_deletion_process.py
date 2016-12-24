#!/usr/bin/python

import os
import datetime
from datetime import timedelta
from dateutil import relativedelta
import json
import traceback
import MySQLdb as mysql
from expiry_report_generator import ExpiryReportGenerator as exp

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (
    convert_to_dict, time_convertion, return_date,
    addMonth, addDays, addYears,
    create_new_date, convert_string_to_date
)

mysqlHost = KNOWLEDGE_DB_HOST
mysqlUser = KNOWLEDGE_DB_USERNAME
mysqlPassword = KNOWLEDGE_DB_PASSWORD
mysqlDatabase = KNOWLEDGE_DATABASE_NAME
mysqlPort = KNOWLEDGE_DB_PORT

seven_years_before_data_download_path = "/seven_years_before_data/download/"
seven_years_before_data_folder_path = "./seven_years_before_data/"

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
            client_connection[d["client_id"]] = db_conn
        except Exception, e :
            print "unable to connect database %s", d
            print e
            continue

    return client_connection

def get_client_database():
    client_list = get_client_db_list()
    client_db = create_client_db_connection(client_list)
    return client_db

def get_new_id(db, table_name, column_name):
    query = "SELECT MAX(%s)+1 FROM %s" % (column_name, table_name)
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()
    if row[0] is None :
        return 1
    return row[0]


def notify_client_regarding_auto_deletion(
    db, download_link, client_id, country_id, domain_id, deletion_date
):
    cursor = db.cursor()

    query = "SELECT group_name FROM tbl_client_groups"
    cursor.execute(query)
    rows = cursor.fetchall()
    group_name = rows[0][0]

    query = "SELECT country_name FROM tbl_countries \
    WHERE country_id = '%d'" % country_id
    cursor.execute(query)
    rows = cursor.fetchall()
    country_name = rows[0][0]

    query = "SELECT domain_name FROM tbl_domains WHERE \
    domain_id = '%d'" % domain_id
    cursor.execute(query)
    rows = cursor.fetchall()
    domain_name = rows[0][0]


    notification_text = '''Dear Client Admin,  \
    Your data and documents before 7 years for %s in the country %s and domain %s \
    will be deleted on %s. Before deletion you can download all the data <a href="%s">here </a> ''' % (
        group_name, country_name, domain_name, deletion_date.date(), download_link
    )
    extra_details = "0 - Auto Deletion"

    if not is_already_notified(db, notification_text, extra_details):
        notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
        created_on = datetime.datetime.now()
        query = "INSERT INTO tbl_notifications_log \
            (notification_id, notification_type_id,\
            notification_text, extra_details, created_on\
            ) VALUES (%s, %s, '%s', '%s', '%s')" % (
                notification_id, 1, notification_text, extra_details, created_on
            )

        cursor.execute(query)
        cursor.close()

        q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
            VALUES (%s, %s)" % (notification_id, 0)
        cur = db.cursor()
        cur.execute(q)

        q = "SELECT username from tbl_admin"
        cur.execute(q)
        rows = cur.fetchall()
        admin_mail_id = rows[0][0]
        cur.close()
        email.notify_auto_deletion(
            admin_mail_id, notification_text
        )

def is_already_notified(
    db, notification_text, extra_details
):
    query = "SELECT count(*) FROM tbl_notifications_log WHERE \
    notification_text = '%s' and extra_details = '%s'" % (
        notification_text, extra_details
    )
    cur = db.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    if rows[0][0] > 0:
        return True
    else:
        return False

def get_configuration_for_client_country(db, country_id):
    query = "SELECT domain_id, period_from FROM tbl_client_configurations\
    WHERE country_id = '%d'" % country_id
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = ["domain_id","period_from"]
    return convert_to_dict(result, columns)

def is_new_year_starting_within_30_days(month, current_date):
    def get_diff_months(year_start_date, current_date):
        r = relativedelta.relativedelta(year_start_date, current_date)
        return r.months
    year_start_date =  datetime.datetime(current_date.year, month, 1)
    no_of_months = get_diff_months(year_start_date, current_date)
    if no_of_months in [1, 0 ]:
        return True
    elif no_of_months < 0:
        year_start_date =  datetime.datetime(current_date.year+1, month, 1)
        no_of_months = get_diff_months(year_start_date, current_date)
        if no_of_months == 1:
            return True
        else: 
            return False
    else:
        return False

def is_seven_years_before_data_available(db, domain_id, country_id):
    query = "SELECT count(*) FROM tbl_compliance_history WHERE  compliance_id in (\
    SELECT compliance_id FROM tbl_client_compliances WHERE client_statutory_id in(\
    SELECT client_statutory_id FROM tbl_client_statutories WHERE country_id = '%d'\
    AND domain_id = '%d')) AND (validity_date < DATE_SUB(now(), INTERVAL 7 YEAR)\
    or validity_date = 0 or validity_date is null) AND due_date < \
    DATE_SUB(now(), INTERVAL 7 YEAR)" % (country_id, domain_id)
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    if result[0][0] > 0:
        return True
    else:
        return False

def delete_data(db, client_id, country_id, domain_id):
    query = "DELETE FROM tbl_compliance_history WHERE  compliance_id in (\
    SELECT compliance_id FROM tbl_client_compliances WHERE client_statutory_id in(\
    SELECT client_statutory_id FROM tbl_client_statutories WHERE country_id = '%d'\
    AND domain_id = '%d')) AND (validity_date < DATE_SUB(now(), INTERVAL 7 YEAR)\
    or validity_date = 0 or validity_date is null) AND due_date < \
    DATE_SUB(now(), INTERVAL 7 YEAR)" % (country_id, domain_id)
    cursor = db.cursor()
    cursor.execute(query)

def bundle_seven_years_before_data(db, client_id, country_id, domain_id):
    download_link = exp(client_id, db).generate_seven_years_before_report(
        country_id, domain_id
    )
    return download_link

def is_current_date_is_deletion_date(period_from, current_date):
    year_start_date = datetime.datetime(current_date.year, period_from, 2)
    if year_start_date == current_date:
        return True
    else:
        return False

def delete_seven_years_before_data(db, client_id, current_date, country_id):
    domain_wise_config = get_configuration_for_client_country(db, country_id)
    domains_to_be_notified = []
    for config in domain_wise_config:
        domain_id = config["domain_id"]
        period_from = config["period_from"]
        if is_new_year_starting_within_30_days(
            period_from, current_date
        ):
            if is_current_date_is_deletion_date(
                period_from, current_date
            ):
                delete_data(db, client_id, country_id, domain_id)
            elif is_seven_years_before_data_available(
                db, domain_id, country_id
            ):
                domains_to_be_notified.append(domain_id)
                download_link = bundle_seven_years_before_data(
                    db, client_id, country_id, domain_id
                )
                deletion_date = datetime.datetime(current_date.year, period_from, 1)
                if deletion_date.date() < current_date:
                    deletion_date = datetime.datetime(current_date.year + 1, period_from, 1)
                notify_client_regarding_auto_deletion(
                    db, download_link, client_id, country_id, domain_id, deletion_date
                )


def run_daily_process(country_id, current_date):
    print '--' * 20
    print "begin daily_process"
    client_info = get_client_database()
    if client_info is not None :
        for client_id, db in client_info.iteritems() :
            try :
                delete_seven_years_before_data(db, client_id, current_date, country_id)
                db.commit()
            except Exception, e :
                print e
                db.rollback()
                print(traceback.format_exc())
    print "end daily_process"
    print '--' * 20

def run_auto_deletion_country_wise():
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
                print info
                break
        if info :
            current_date = return_date(time_convertion(info.get("timezones")[0]))
            print "country -- ", c["country_name"]
            print
            run_daily_process(c["country_id"], current_date)
