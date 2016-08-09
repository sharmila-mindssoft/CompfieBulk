#!/usr/bin/python

import datetime
import json
import traceback
import threading
from server import logger
from datetime import timedelta
from server.dbase import Database
from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (
    convert_to_dict, time_convertion, return_date,
    addMonth, addDays, addYears,
    create_new_date, convert_string_to_date,
)
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
email = EmailHandler()

class KnowledgeConnect(object):
    def __init__(self):
        self._k_db = None
        self.get_knowledge_connect()

    def get_knowledge_connect(self):
        self._k_db = Database(
            KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT,
            KNOWLEDGE_DB_USERNAME, KNOWLEDGE_DB_PASSWORD,
            KNOWLEDGE_DATABASE_NAME
        )
        self._k_db.connect()

    def get_countries(self):
        try:
            self._k_db.begin()
            q = "SELECT country_id, country_name FROM tbl_countries"
            rows = self._k_db.select_all(q)
            self._k_db.commit()
            return convert_to_dict(rows, ["country_id", "country_name"])
        except Exception, e:
            print e
            self._k_db.rollback()

    def get_client_db_list(self):
        try :
            self._k_db.begin()
            query = "SELECT T1.client_id, T1.database_ip, T1.database_port, \
                T1.database_username, T1.database_password, T1.database_name \
                FROM tbl_client_database T1"
            rows = self._k_db.select_all(query)
            self._k_db.commit()
            if rows :
                columns = [
                    "client_id", "database_ip", "database_port", "database_username",
                    "database_password", "database_name"
                ]
                result = convert_to_dict(rows, columns)
                return result
            else :
                return None

        except Exception, e :
            print e
            self._k_db.rollback()
            print (traceback.format_exc())


class AutoStart(Database):
    def __init__(self, c_db_ip, c_db_username, c_db_password, c_db_name, c_db_port, client_id, current_date):
        super(AutoStart, self).__init__(
            c_db_ip, c_db_port, c_db_username, c_db_password, c_db_name
        )
        self.connect()
        self.client_id = client_id
        self.current_date = current_date

    def get_email_id_for_users(self, user_id):
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s"
        row = self.select_one(q, [user_id])
        if row :
            return row[0], row[1]
        else :
            return None

    def get_compliance_to_start(self):
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
            WHERE (t1.due_date - INTERVAL t1.trigger_before_days DAY) <= %s \
            AND t1.is_active = 1 AND t2.is_active = 1 \
            AND t4.compliance_id is null "
        rows = self.select_all(query, [self.current_date])
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

    def calculate_next_due_date(
        self, frequency, statutory_dates, repeat_type,
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

    def save_in_compliance_history(
        self, unit_id, compliance_id, start_date, due_date, next_due_date,
        assignee, concurrence, approve
    ):
        # compliance_history_id = get_new_id(db, "tbl_compliance_history", "compliance_history_id")
        if concurrence is not None:
            values = (
                unit_id, compliance_id,
                start_date, due_date, next_due_date, assignee, approve, concurrence
            )
            query = "INSERT INTO tbl_compliance_history (unit_id, compliance_id, \
                start_date, due_date, next_due_date, completed_by, approved_by, concurred_by) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "

        else :
            values = (
                unit_id, compliance_id,
                start_date, due_date, next_due_date, assignee, approve
            )

            query = "INSERT INTO tbl_compliance_history (unit_id, compliance_id, \
                start_date, due_date, next_due_date, completed_by, approved_by) \
                VALUES (%s, %s, %s, %s, %s, %s, %s) "

        compliance_history_id = self.execute_insert(query, values)
        return compliance_history_id

    def update_assign_compliance_due_date(self, trigger_before, due_date, unit_id, compliance_id):
        query = "UPDATE tbl_assigned_compliances set due_date= %s, \
            trigger_before_days= %s \
            WHERE unit_id = %s AND compliance_id = %s "
        self.execute(query, [due_date, trigger_before, unit_id, compliance_id])

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None  :
                q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
                    VALUES (%s, %s)"
                self.execute(q, [notification_id, user_id])

        # notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
        created_on = datetime.datetime.now()
        column = [
                "country_id", "domain_id",
                "legal_entity_id", "unit_id", "compliance_id",
                "assignee", "approval_person", "notification_type_id",
                "notification_text", "extra_details", "created_on"
            ]
        values = [
            country_id, domain_id,
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

        notification_id = self.insert("tbl_notifications_log", column, values)
        if notification_id is False :
            return False

        save_notification_users(notification_id, assignee)
        if notify_to_all:
            if approval_person is not None and assignee != approval_person:
                save_notification_users(notification_id, approval_person)
            if concurrence_person is not None or concurrence_person is not "NULL" :
                save_notification_users(notification_id, concurrence_person)

    def start_new_task(self):
        def notify(d, due_date, next_due_date, approval_person):
            compliance_history_id = self.save_in_compliance_history(
                int(d["unit_id"]), int(d["compliance_id"]), self.current_date,
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
            self.save_in_notification(
                d["country_id"], d["domain_id"], d["business_group_id"], d["legal_entity_id"],
                d["division_id"], d["unit_id"], d["compliance_id"], d["assignee"],
                d["concurrence_person"], d["approval_person"],
                notification_text, extra_details, notification_type_id
            )
            a_name, assignee_email = self.get_email_id_for_users(d["assignee"])
            notify_new_task = threading.Thread(
                target=email.notify_compliance_start,
                args=[
                    a_name, compliance_name, unit_name,
                    d["due_date"], assignee_email
                ]
            )
            notify_new_task.start()

        def start_next_due_date_task(d, due_date, approval_person) :
            next_due_date, trigger_before = self.calculate_next_due_date(
                d["frequency"], d["statutory_dates"], d["repeat_type_id"],
                d["repeats_every"], due_date
            )

            if trigger_before is None:
                trigger_before = int(d["trigger_before_days"])

            notify(d, due_date, next_due_date, approval_person)
            return next_due_date, trigger_before

        data = self.get_compliance_to_start()
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
                    self.update_assign_compliance_due_date(trigger_before, next_due_date, d["unit_id"], d["compliance_id"])
                    print next_due_date
                    if next_due_date is not None :
                        while (next_due_date - timedelta(days=trigger_before)) <= self.current_date :
                            # start for next-due-date
                            next_due_date, trigger_before = start_next_due_date_task(d, next_due_date, approval_person)
                            print next_due_date, trigger_before
                            self.update_assign_compliance_due_date(trigger_before, next_due_date, d["unit_id"], d["compliance_id"])

                count += 1
            except Exception, e :
                print e
                continue
                # print(traceback.format_exc())

        print " %s compliances started for client_id %s - %s" % (count, self.client_id, self.current_date)

    def check_service_provider_contract_period(self):
        query = "UPDATE tbl_service_providers set is_active = 0 WHERE \
        contract_from >= now() and contract_to <= now()"
        self.execute(query)

    def start_process(self):
        try :
            self.begin()
            self.start_new_task()
            self.check_service_provider_contract_period()
            self.commit()
        except Exception, e :
            print e
            logger.logProcessError("DailyProcess", (traceback.format_exc()))
            self.rollback()
            self.close()


class DailyProcess(KnowledgeConnect):
    def __init__(self):
        super(DailyProcess, self).__init__()

    def begin_process(self):
        current_date = datetime.datetime.utcnow().date()
        client_info = self.get_client_db_list()
        for c in client_info:
            try :
                task = AutoStart(
                    c["database_ip"], c["database_username"],
                    c["database_password"], c["database_name"],
                    c["database_port"], c["client_id"], current_date
                )
                task.start_process()
            except Exception, e :
                print e
                logger.logProcessError("DailyProcess", e)
                logger.logProcessError("DailyProcess", (traceback.format_exc()))

def run_daily_process():
    dp = DailyProcess()
    dp.begin_process()
