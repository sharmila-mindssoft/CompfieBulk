#!/usr/bin/python

import datetime
import json
import traceback
import threading
from datetime import timedelta
from dateutil import relativedelta
from processes.process_logger import logProcessError, logProcessInfo
from processes.process_dbase import Database
# from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (

    # time_convertion, return_date,
    addMonth, addDays, addYears,
    create_new_date, convert_string_to_date,
)
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
email = EmailHandler()

__all__ = [
    "KnowledgeConnect"
]

def getCurrentYear():
    now = datetime.datetime.now()
    return now.year


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

    def get_knowledge_close(self):
        if self._k_db is not None :
            self._k_db.close()

    def get_countries(self):
        try:
            self._k_db.begin()
            q = "SELECT country_id, country_name FROM tbl_countries"
            rows = self._k_db.select_all(q)

            self._k_db.commit()
            return rows
        except Exception, e:
            logProcessError("get_countries", str(e))
            self._k_db.rollback()

    def get_client_db_list(self):
        try :
            self._k_db.begin()
            query = "select t1.client_id, t1.legal_entity_id, " + \
                    " t2.database_username, t2.database_password, t2.database_name, " + \
                    " t3.database_ip, t3.database_port, " + \
                    " t4.ip as file_ip, t4.port as file_port " + \
                    " from tbl_client_database as t1 " + \
                    " inner join tbl_client_database_info as t2 " + \
                    " on t1.client_database_id = t2.client_database_id and t2.is_group = 0 " + \
                    " inner join tbl_database_server as t3 " + \
                    " on t1.database_server_id = t3.database_server_id " + \
                    " inner join tbl_file_server as t4 on " + \
                    " t1.file_server_id = t4.file_server_id "
            logProcessInfo("client_db_list", str(query))
            rows = self._k_db.select_all(query)
            self._k_db.commit()
            if rows :
                return rows
            else :
                return []

        except Exception, e :
            print e
            logProcessError("get_clients", str(e))
            self._k_db.rollback()
            logProcessError("get_clients", str(traceback.format_exc()))

    def get_deletion_period(self, le_id, encode=True):
        try :
            self._k_db.begin()
            query = "select distinct deletion_period from tbl_auto_deletion where legal_entity_id = %s"
            rows = self._k_db.select_all(query, [le_id])
            if rows :
                if len(rows) > 1 :
                    q = "select client_id, legal_entity_id, unit_id, deletion_period from tbl_auto_deletion where legal_entity_id = %s"
                    rows = self._k_db.select_all(q, [le_id])
            self._k_db.commit()
        except Exception, e :
            self._k_db.rollback()
            print e
        finally :
            if rows :
                if encode :
                    rows = json.dumps(rows)
                    rows = rows.encode('base64')
                    return rows
                else :
                    return rows
            else :
                return None

    def get_configuration_for_client_country(self, le_id):
        try :
            self._k_db.begin()
            query = "SELECT t1.domain_id, t1.month_from FROM tbl_client_configuration as t1 " + \
                " inner join tbl_legal_entities as t2 on t2.country_id = t1.country_id " + \
                "WHERE t2.legal_entity_id = %s"
            rows = self.select_all(query, [le_id])
            return rows
            self._k_db.commit()
        except Exception, e :
            self._k_db.rollback()
            print e

    def is_new_year_starting_within_30_days(self, month):
        def get_diff_months(year_start_date):
            r = relativedelta.relativedelta(year_start_date, self.current_date)
            return r.months
        year_start_date = datetime.datetime(self.current_date.year, month, 1)
        no_of_months = get_diff_months(year_start_date)
        print no_of_months
        if no_of_months in [1, 0]:
            return True
        elif no_of_months < 0:
            year_start_date = datetime.datetime(self.current_date.year+1, month, 1)
            no_of_months = get_diff_months(year_start_date)
            if no_of_months == 1:
                return True
            else:
                return False
        else:
            return False

    def is_current_date_is_deletion_date(self, period_from):
        year_start_date = datetime.datetime(self.current_date.year, period_from, 2)
        if year_start_date == self.current_date:
            return True
        else:
            return False

class AutoStart(Database):
    def __init__(
        self, c_db_ip, c_db_username, c_db_password, c_db_name, c_db_port,
        client_id, legal_entity_id, current_date
    ):
        super(AutoStart, self).__init__(
            c_db_ip, c_db_port, c_db_username, c_db_password, c_db_name
        )
        self._c_db_ip = c_db_ip
        self._c_db_name = c_db_name
        self.connect()
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.current_date = current_date
        self.started_unit_id = []
        self.started_user_id = []

    def get_email_id_for_users(self, user_id):
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s"
        logProcessInfo("user_email_id", q % (user_id))
        row = self.select_one(q, [user_id])
        if row :
            return row["employee_name"], row["email_id"]
        else :
            return None

    def get_compliance_to_start(self):
        query = "SELECT t1.country_id, t1.unit_id, t1.compliance_id, t1.statutory_dates, " + \
            " t1.trigger_before_days, t1.due_date, t1.validity_date, " + \
            " t2.document_name, t2.compliance_task, t2.frequency_id, t2.repeats_type_id," + \
            " t2.repeats_every, (t1.due_date - INTERVAL t1.trigger_before_days DAY) start_date," + \
            " t3.unit_id, t3.unit_code, t3.unit_name, t3.business_group_id, " + \
            " t3.legal_entity_id, t3.division_id, t2.domain_id, " + \
            " t1.assignee, t1.concurrence_person, t1.approval_person, " + \
            " t1.compliance_id " + \
            " from tbl_assign_compliances t1 " + \
            " INNER JOIN tbl_legal_entities as t5  on t1.legal_entity_id = t5.legal_entity_id and t5.is_closed = 0 and t5.contract_to > %s " + \
            " INNER JOIN tbl_units t3 on t1.unit_id = t3.unit_id and t3.is_closed = 0 " + \
            " INNER JOIN tbl_compliances t2 on t1.compliance_id = t2.compliance_id " + \
            " LEFT JOIN tbl_compliance_history t4 ON (t4.unit_id = t1.unit_id " + \
            "     AND t4.compliance_id = t1.compliance_id AND t2.frequency_id = 1)" + \
            " WHERE (t1.due_date - INTERVAL t1.trigger_before_days DAY) <= %s " + \
            " AND t1.is_active = 1 AND t2.is_active = 1 AND t2.frequency_id < 5 " + \
            " AND t4.compliance_id is null "

        logProcessInfo("compliance_to_start %s" % self.client_id, query % (self.current_date, self.current_date))
        rows = self.select_all(query, [self.current_date, self.current_date])
        print query % (self.current_date, self.current_date)
        return rows

    def calculate_next_due_date(
        self, frequency, statutory_dates, repeat_type,
        repeat_every, old_due_date
    ):
        # frequency 1: One Time, 2 : Periodical, 3 : Review, 4: On occurance
        #  repeat_type 1 : Days, 2 : Months, 3 : years

        statutory_dates = json.loads(statutory_dates)
        trigger_before_days = None
        if statutory_dates == []:
            statutory_dates = None
        print "FREQUENCY----------", frequency
        if frequency == 2 or frequency == 3 or frequency == 4:
            repeat_every = int(repeat_every)
            repeat_type = int(repeat_type)
            if statutory_dates is None or len(statutory_dates) == 1 :
                if repeat_type == 1 :
                    new_due_date = addDays(repeat_every, old_due_date)
                elif repeat_type == 2 :
                    new_due_date = addMonth(repeat_every, old_due_date)
                elif repeat_type == 3 :
                    new_due_date = addYears(repeat_every, old_due_date)
                else :
                    print "repeat_type not matched"
                    new_due_date = old_due_date
                return (new_due_date,  trigger_before_days)
            else :
                temp_date = convert_string_to_date(str(old_due_date))
                old_month = temp_date.month
                repeat_type = int(repeat_type)
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
                self.legal_entity_id, unit_id, compliance_id,
                start_date, due_date, next_due_date, assignee, approve, concurrence
            )
            query = "INSERT INTO tbl_compliance_history (legal_entity_id, unit_id, compliance_id, " + \
                " start_date, due_date, next_due_date, completed_by, approved_by, concurred_by) " + \
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "

        else :
            values = (
                self.legal_entity_id, unit_id, compliance_id,
                start_date, due_date, next_due_date, assignee, approve
            )

            query = "INSERT INTO tbl_compliance_history (legal_entity_id, unit_id, compliance_id, " + \
                " start_date, due_date, next_due_date, completed_by, approved_by) " + \
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "

        logProcessInfo("save_new_compliance %s" % self.client_id, query % values)

        compliance_history_id = self.execute_insert(query, values)
        return compliance_history_id

    def update_assign_compliance_due_date(self, trigger_before, due_date, unit_id, compliance_id):
        query = "UPDATE tbl_assign_compliances set due_date= %s, " + \
            " trigger_before_days= %s " + \
            " WHERE unit_id = %s AND compliance_id = %s "
        values = (due_date, trigger_before, unit_id, compliance_id)
        logProcessInfo("update_assigne_compliance", query % values)
        self.execute(query, values)

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None  :
                q = "INSERT INTO tbl_notifications_user_log(notification_id, user_id) " + \
                    " VALUES (%s, %s) "
                v = (notification_id, user_id)
                logProcessInfo("save_notification_user %s" % self.client_id, q % v)
                self.execute(q, v)

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

    def actual_start_date(self, due_date, trigger_before):
        if due_date is not None and trigger_before is not None :
            d = due_date - timedelta(days=int(trigger_before))
            return d
        else :
            return None

    def is_this_first_task_of_year(self, unit_id, country_id, domain_id, compliance_id):
        q = "select month_from, month_to from tbl_client_configuration where country_id = %s and domain_id = %s"
        c_row = self.select_one(q, [country_id, domain_id])

        print "\n"
        print q % (country_id, domain_id)
        print c_row

        years = []
        if c_row["month_from"] == 1 and c_row["month_to"] == 12 :
            years = [getCurrentYear(), 1, getCurrentYear(), 2]
        else :
            years = [getCurrentYear(), c_row["month_from"], getCurrentYear()+1, c_row["month_to"]]

        q1 = "select count(0) comp_count from tbl_compliance_history where unit_id = %s and compliance_id = %s " + \
            " and due_date >= date(concat_ws('-',%s,%s,1))  " + \
            " and due_date <= last_day(date(concat_ws('-',%s,%s,1))) "
        param = [unit_id, compliance_id]
        param.extend(years)
        rows = self.select_one(q1, param)

        print q1 % tuple(param)
        print rows

        if rows :
            cnt = rows["comp_count"]
        else :
            cnt = 0

        statutory_date = None
        repeats_every = None
        repeats_type_id = None

        if cnt == 0 :
            print "count == 0"

            q1 = "select repeats_type_id, repeats_every, statutory_date, trigger_before_days, due_date from tbl_compliance_dates where " + \
                "compliance_id = %s and unit_id = %s "
            d_rows = self.select_one(q1, [compliance_id, unit_id])

            print q1 % (compliance_id, unit_id)
            print d_rows

            if d_rows :
                repeats_type_id = d_rows["repeats_type_id"]
                repeats_every = d_rows["repeats_every"]
                statutory_date = d_rows["statutory_date"]
                due_date = d_rows["due_date"]
                trigger_days = d_rows["trigger_before_days"]
                if statutory_date is not None :
                    qq = "update tbl_assign_compliances set statutory_dates = %s, trigger_before_days = %s, due_date = %s " + \
                        " where compliance_id = %s and unit_id = %s"
                    print qq % (statutory_date, trigger_days, due_date, compliance_id, unit_id)
                    self.execute(qq, [statutory_date, trigger_days, due_date, compliance_id, unit_id])
            else :
                q1 = "select repeats_type_id, repeats_every, statutory_dates, trigger_before_days, due_date from tbl_assign_compliances where " + \
                    "compliance_id = %s and unit_id = %s "
                d_rows = self.select_one(q1, [compliance_id, unit_id])
                if d_rows :
                    repeats_type_id = d_rows["repeats_type_id"]
                    repeats_every = d_rows["repeats_every"]
                    statutory_date = d_rows["statutory_dates"]
                    due_date = d_rows["due_date"]
                    trigger_days = d_rows["trigger_before_days"]

        else :
            q1 = "select repeats_type_id, repeats_every, statutory_dates, trigger_before_days, due_date from tbl_assign_compliances where " + \
                "compliance_id = %s and unit_id = %s "
            d_rows = self.select_one(q1, [compliance_id, unit_id])

            if d_rows :
                repeats_type_id = d_rows["repeats_type_id"]
                repeats_every = d_rows["repeats_every"]
                statutory_date = d_rows["statutory_dates"]
                due_date = d_rows["due_date"]
                trigger_days = d_rows["trigger_before_days"]

        print cnt, statutory_date, repeats_every, repeats_type_id
        return cnt, statutory_date, repeats_every, repeats_type_id

    def start_new_task(self):
        def notify(d, due_date, next_due_date, approval_person, trigger_before):
            start_date = self.actual_start_date(due_date, trigger_before)

            compliance_history_id = self.save_in_compliance_history(
                int(d["unit_id"]), int(d["compliance_id"]), start_date,
                due_date, next_due_date, int(d["assignee"]),
                d["concurrence_person"], int(approval_person)
            )
            if compliance_history_id is False :
                return False
            else :
                self.started_unit_id.append(d["unit_id"])
                self.started_user_id.append(d["assignee"])
                self.started_user_id.append(approval_person)
                self.started_user_id.append(d["concurrence_person"])

            if d["document_name"] :
                compliance_name = d["document_name"] + " - " + d["compliance_task"]
            else :
                compliance_name = d["compliance_task"]
            unit_name = d["unit_code"] + " - " + d["unit_name"]
            notification_text = "Compliance task %s started" % (compliance_name)
            extra_details = " %s - Compliance Started" % (compliance_history_id)
            notification_type_id = 4   # 4 = messages
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
            return True

        def start_next_due_date_task(d, due_date, approval_person) :
            next_due_date, trigger_before = self.calculate_next_due_date(
                int(d["frequency_id"]), d["statutory_dates"], d["repeats_type_id"],
                d["repeats_every"], due_date
            )

            if trigger_before is None:
                trigger_before = int(d["trigger_before_days"])

            c_h_id = notify(d, due_date, next_due_date, approval_person, trigger_before)
            if c_h_id is False :
                logProcessError("next_due_date_task %s" % self.client_id, "compliance history save failed for %s" % (next_due_date))
                logProcessError("next_due_date_task %s " % self.client_id, str(d))
                return None, trigger_before
            return next_due_date, trigger_before

        data = self.get_compliance_to_start()
        count = 0
        for d in data :
            print d["unit_id"]
            try :
                approval_person = int(d["approval_person"])
                if d["frequency_id"] == 1 :
                    next_due_date = "0000-00-00"
                    trigger_before = d["trigger_before_days"]
                    if trigger_before is None :
                        continue
                    c_h_id = notify(d, d["due_date"], next_due_date, approval_person, trigger_before)
                    if c_h_id is False :
                        # compliance history id is false so continue further
                        continue
                else:
                    if d["frequency_id"] in [3, 4] :
                        cnt, statutory_date, repeats_every, repeats_type_id = self.is_this_first_task_of_year(d["unit_id"], d["country_id"], d["domain_id"], d["compliance_id"])
                        if statutory_date is None and repeats_every is None and repeats_type_id is None :
                            continue
                        else :
                            d["statutory_dates"] = statutory_date
                            d["repeats_type_id"] = repeats_type_id
                            d["repeats_every"] = repeats_every

                    next_due_date = trigger_before = None
                    due_date = d["due_date"]
                    print due_date
                    next_due_date, trigger_before = start_next_due_date_task(d, due_date, approval_person)
                    print next_due_date
                    if next_due_date is not None :
                        self.update_assign_compliance_due_date(trigger_before, next_due_date, d["unit_id"], d["compliance_id"])
                        while (next_due_date - timedelta(days=trigger_before)) <= self.current_date :
                            # start for next-due-date
                            next_due_date, trigger_before = start_next_due_date_task(d, next_due_date, approval_person)
                            if next_due_date is None :
                                break
                            self.update_assign_compliance_due_date(trigger_before, next_due_date, d["unit_id"], d["compliance_id"])

                count += 1
            except Exception, e :
                logProcessError("task_start_failed", str(e))
                logProcessError("task_start_failed", d)
                logProcessError("task_start_failed", str(traceback.format_exc()))
                continue

        print_msg = " %s compliances started for client_id %s - %s" % (count, self.client_id, self.current_date)
        logProcessInfo("start_new_task %s" % self.client_id, str(print_msg))

    def check_service_provider_contract_period(self):
        query = "UPDATE tbl_service_providers set is_active = 0 WHERE " + \
            " contract_from >= now() and contract_to <= now() "
        try :
            self.execute(query)
            logProcessInfo("check_service_provider_contract_period %s" % self.client_id, str(query))
        except Exception, e :
            logProcessError("check_service_provider_contract_period %s" % self.client_id, str(e))

    def get_year_to_update_chart(self):
        q = "select distinct t1.country_id, t1.domain_id, t1.chart_year, t1.month_from, t1.month_to from tbl_compliance_status_chart_unitwise as t1" + \
            " inner join tbl_client_configuration as t2 on t1.country_id = t2.country_id and t1.domain_id = t2.domain_id " + \
            " and t1.month_from = t2.month_from and t1.month_to = t2.month_to " + \
            " where t1.inprogress_count > 0 or t1.overdue_count > 0"
        rows = self.select_all(q)
        years = []
        for r in rows :
            years.append(r["chart_year"])
        return years

    def get_client_date_configuration(self):
        q = "select country_id, domain_id, month_from, month_to from tbl_client_configuration "
        rows = self.select_all(q)
        return rows

    def update_unit_wise_task_status(self):
        q_delete = "delete from tbl_compliance_status_chart_unitwise where chart_year = %s and domain_id = %s and country_id = %s "
        # unit_ids = ",".join([str(x) for x in self.started_unit_id])
        dat_conf = self.get_client_date_configuration()
        year = self.get_year_to_update_chart()

        year.append(getCurrentYear() - 2)
        year.append(getCurrentYear() - 1)
        year.append(getCurrentYear())

        q = "insert into tbl_compliance_status_chart_unitwise( " + \
            "     legal_entity_id, country_id, domain_id, unit_id,  " + \
            "     month_from, month_to, chart_year, complied_count, delayed_count, inprogress_count, overdue_count " + \
            " ) " + \
            " select unt.legal_entity_id, ccf.country_id,ccf.domain_id, " + \
            " ch.unit_id,ccf.month_from,ccf.month_to, %s, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= ch.completion_date, date(ch.due_date) >= date(ch.completion_date)) " + \
            " and ifnull(ch.approve_status,0) = 1, 1, 0)) as complied_count, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < ch.completion_date, date(ch.due_date) < date(ch.completion_date)) and " + \
            " ifnull(ch.approve_status,0) = 1, 1, 0)) as delayed_count, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ifnull(ch.approve_status, 0) <> 1  " + \
            " and ifnull(ch.approve_status,0) <> 3, 1, 0)) as inprogress_count, " + \
            " sum(IF((IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < now(), ch.due_date < curdate())  " + \
            " and ifnull(ch.approve_status,0) <> 1) or ifnull(ch.approve_status,0) = 3, 1, 0)) as overdue_count " + \
            " from tbl_client_configuration as ccf " + \
            " inner join tbl_units as unt on ccf.country_id = unt.country_id and ccf.client_id = unt.client_id  " + \
            " inner join tbl_client_compliances as cc on unt.unit_id = cc.unit_id and ccf.domain_id = cc.domain_id  " + \
            " inner join tbl_compliances as com on cc.compliance_id = com.compliance_id and ccf.domain_id = com.domain_id " + \
            " left join tbl_compliance_history as ch on ch.unit_id = cc.unit_id and ch.compliance_id = cc.compliance_id " + \
            " where ch.due_date >= date(concat_ws('-',%s,ccf.month_from,1))  " + \
            " and ch.due_date <= last_day(date(concat_ws('-',%s,ccf.month_to,1))) " + \
            " and ccf.country_id = %s and ccf.domain_id = %s " + \
            " group by ccf.country_id,ccf.domain_id,ccf.month_from,ccf.month_to,ch.unit_id " + \
            " on duplicate key update complied_count = values(complied_count), " + \
            " delayed_count = values(delayed_count), inprogress_count = values(inprogress_count), " + \
            " overdue_count = values(overdue_count) "

        for y in year :
            for d in dat_conf :
                c_id = d["country_id"]
                d_id = d["domain_id"]

                from_year = y
                if d["month_from"] == 1 and d["month_to"] == 12 :
                    to_year = y
                else :
                    to_year = y+1
                print q % (y, from_year, to_year, c_id, d_id)
                print "\n"
                self.execute(q_delete, [y, d_id, c_id])
                self.execute(q, [y, from_year, to_year, c_id, d_id])
                print q, tuple([y, from_year, to_year, c_id, d_id])
                # if c_id == y["country_id"] and d_id == y["domain_id"] :
                #     self.execute(q, [y, from_year, to_year, c_id, d_id])
                # else :
                #     continue

    def update_user_wise_task_status(self):
        # unit_ids = ",".join([str(x) for x in self.started_unit_id])
        # user_ids = ",".join([str(y) for y in self.started_user_id])
        dat_conf = self.get_client_date_configuration()
        year = self.get_year_to_update_chart()
        year.append(getCurrentYear() - 1)
        year.append(getCurrentYear() - 2)
        year.append(getCurrentYear())

        q = "insert into tbl_compliance_status_chart_userwise( " + \
            "     legal_entity_id, country_id, domain_id, unit_id, user_id, " + \
            "     month_from, month_to, chart_year, complied_count, delayed_count, inprogress_count, overdue_count " + \
            " ) " + \
            " select unt.legal_entity_id, ccf.country_id,ccf.domain_id, ch.unit_id, usr.user_id, " + \
            " ccf.month_from,ccf.month_to,%s, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= ch.completion_date, date(ch.due_date) >= date(ch.completion_date)) " + \
            " and ifnull(ch.approve_status,0) = 1, 1, 0)) as complied_count, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < ch.completion_date, date(ch.due_date) < date(ch.completion_date)) and " + \
            " ifnull(ch.approve_status,0) = 1, 1, 0)) as delayed_count, " + \
            " sum(IF(IF(ifnull(com.duration_type_id,0) = 2, ch.due_date >= now(), date(ch.due_date) >= curdate()) and ifnull(ch.approve_status, 0) <> 1  " + \
            " and ifnull(ch.approve_status,0) <> 3, 1, 0)) as inprogress_count, " + \
            " sum(IF((IF(ifnull(com.duration_type_id,0) = 2, ch.due_date < now(), ch.due_date < curdate())  " + \
            " and ifnull(ch.approve_status,0) <> 1) or ifnull(ch.approve_status,0) = 3, 1, 0)) as overdue_count " + \
            " from tbl_client_configuration as ccf " + \
            " inner join tbl_units as unt on ccf.country_id = unt.country_id and ccf.client_id = unt.client_id " + \
            " inner join tbl_client_compliances as cc on unt.unit_id = cc.unit_id and ccf.domain_id = cc.domain_id " + \
            " inner join tbl_compliances as com on cc.compliance_id = com.compliance_id " + \
            " left join tbl_compliance_history as ch on ch.unit_id = cc.unit_id and ch.compliance_id = cc.compliance_id " + \
            " inner join tbl_users as usr on usr.user_id = ch.completed_by OR usr.user_id = ch.concurred_by OR usr.user_id = ch.approved_by " + \
            " where ch.due_date >= date(concat_ws('-',%s,ccf.month_from,1))  " + \
            " and ch.due_date <= last_day(date(concat_ws('-',%s,ccf.month_to,1))) " + \
            " and ccf.country_id = %s and ccf.domain_id = %s " + \
            " group by ccf.country_id,ccf.domain_id, ch.unit_id, ccf.month_from,ccf.month_to,usr.user_id " + \
            " on duplicate key update complied_count = values(complied_count), " + \
            " delayed_count = values(delayed_count), inprogress_count = values(inprogress_count), " + \
            " overdue_count = values(overdue_count) "

        # if len(self.started_unit_id) > 0 :
        # self.execute(q_delete, [years])
        for y in year :
            for d in dat_conf :
                c_id = d["country_id"]
                d_id = d["domain_id"]
                from_year = y
                if d["month_from"] == 1 and d["month_to"] == 12 :
                    to_year = y
                else :
                    to_year = y+1
                self.execute(q, [y, from_year, to_year, c_id, d_id])
                # if c_id == y["country_id"] and d_id == y["domain_id"] :
                #     self.execute(q, [y, from_year, to_year, c_id, d_id])
                # else :
                #     continue

    def update_duedate_in_calendar_view(self):
        q = "insert into tbl_calendar_view(legal_entity_id, user_id, year, month, date, due_date_count) " + \
            "select t.legal_entity_id, t.completed_by, t.du_year, t.du_month, t.du_date, t.du_count " + \
            " from ( " + \
            " select ch.legal_entity_id, ch.unit_id, ch.completed_by, day(ch.due_date) as du_date,  " + \
            " month(ch.due_date) as du_month, year(ch.due_date) as du_year,  " + \
            " count(compliance_history_id) du_count " + \
            " from tbl_compliance_history as ch " + \
            " where current_status = 0 " + \
            " and ch.due_date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
            " group by ch.completed_by, day(due_date), month(ch.due_date), year(ch.due_date) " + \
            " order by year(ch.due_date), month(ch.due_date), day(due_date) " + \
            " ) as t " + \
            " on duplicate key update due_date_count = t.du_count"

        self.execute(q)

    def update_upcoming_in_calendar_view(self):
        self.execute("delete from tbl_calendar_view where date < day(now())")

        q = "insert into tbl_calendar_view (legal_entity_id, user_id, year, month, date, upcoming_count) " + \
            " select t.legal_entity_id, t.assignee, t.up_year, t.up_month, t.up_date, t.up_count " + \
            " from ( " + \
            " select ac.legal_entity_id, ac.assignee, " + \
            " day(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_date, " + \
            " month(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_month, " + \
            " year(DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY)) as up_year, " + \
            " count(ac.compliance_id) as up_count " + \
            " from tbl_assign_compliances as ac " + \
            " inner join tbl_compliances as com on ac.compliance_id = com.compliance_id and com.frequency_id != 5 " + \
            " where DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) > curdate() " + \
            " AND ac.due_Date < DATE_ADD(now(), INTERVAL 6 MONTH) " + \
            " group by ac.assignee, DATE_SUB(ac.due_date, INTERVAL ac.trigger_before_days DAY) " + \
            " ) as t " + \
            " on duplicate key update upcoming_count = t.up_count; "
        self.execute(q)

    def start_process(self):
        if self._connection is None :
            details = "%s, %s" % (self._c_db_ip, self._c_db_name)
            logProcessInfo("connection not found %s" % self.client_id, details)
            return
        try :
            self.begin()
            self.start_new_task()
            self.check_service_provider_contract_period()
            self.update_unit_wise_task_status()
            self.update_user_wise_task_status()
            self.update_duedate_in_calendar_view()
            self.update_upcoming_in_calendar_view()
            self.commit()
            self.close()
        except Exception, e :
            logProcessError("start_process %s" % self.client_id, str(e))
            logProcessError("start_process", str(traceback.format_exc()))
            logProcessError("start_process", (traceback.format_exc()))
            self.rollback()
            self.close()

class DailyProcess(KnowledgeConnect):
    def __init__(self):
        super(DailyProcess, self).__init__()

    def begin_process(self):
        current_date = datetime.datetime.utcnow().date()
        client_info = self.get_client_db_list()
        logProcessInfo("DailyProcess", "process begin")
        logProcessInfo("DailyProcess", str(current_date))
        logProcessInfo("begin_process", client_info)
        try :
            for c in client_info:
                print c
                try :
                    task = AutoStart(
                        c["database_ip"], c["database_username"],
                        c["database_password"], c["database_name"],
                        c["database_port"], c["client_id"], c["legal_entity_id"], current_date
                    )
                    task.start_process()

                except Exception, e :
                    logProcessError("DailyProcess", e)
                    logProcessError("DailyProcess", (traceback.format_exc()))
        except Exception, e :
            print e

        finally :
            self.get_knowledge_close()

def run_daily_process():
    dp = DailyProcess()
    dp.begin_process()
