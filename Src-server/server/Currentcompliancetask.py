import json
import threading
import datetime
from datetime import timedelta
from database import Database
from server.emailcontroller import EmailHandler
from server.common import (
    create_new_date, addMonth, addDays,
    addYears, convert_string_to_date

)
__all__ = [
    "ComplianceTask"
]
email = EmailHandler()

class ComplianceTask(Database):
    def __init__(
        self, host, port, username,
        password, database_name
    ):
        super(ComplianceTask, self).__init__(
            host, port, username, password,
            database_name
        )

    def get_compliance_to_start(self, current_date, country_id):
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
            AND t4.compliance_id is null "

        rows = self.select_all(query, [current_date, country_id])
        columns = [
            "country_id", "unit_id", "compliance_id", "statutory_dates",
            "trigger_before_days", "due_date", "validity_date", "document_name", "compliance_task",
            "frequency", "repeat_type_id", "repeats_every", "start_date",
            "unit_id", "unit_code", "unit_name",
            "business_group_id", "legal_entity_id", "division_id",
            "domain_id",
            "assignee", "concurrence_person", "approval_person", "t4_compliance_id"
        ]
        result = self.convert_to_dict(rows, columns)

        return result

    def get_email_id_for_users(self, user_id):
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s"
        row = self.select_one(q, [user_id])
        if row :
            return row[0], row[1]
        else :
            return None

    def save_in_compliance_history(
        self, unit_id, compliance_id, start_date, due_date, next_due_date,
        assignee, concurrence, approve
    ):
        compliance_history_id = self.get_new_id("compliance_history_id", "tbl_compliance_history")
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

        self.execute(query)
        return compliance_history_id

    def update_assign_compliance_due_date(self, trigger_before, due_date, unit_id, compliance_id):
        query = "UPDATE tbl_assigned_compliances set due_date='%s', trigger_before_days=%s \
            WHERE unit_id = %s AND compliance_id = %s \
            " % (due_date, trigger_before, unit_id, compliance_id)
        # print query
        self.execute(query)

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
                    new_due_date = None
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

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None :
                q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
                    VALUES (%s, %s)" % (notification_id, user_id)
                self.execute(q)

        notification_id = self.get_new_id("notification_id", "tbl_notifications_log")
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

        self.insert("tbl_notifications_log", column, values)
        save_notification_users(notification_id, assignee)
        if notify_to_all:
            if approval_person is not None and assignee != approval_person:
                save_notification_users(notification_id, approval_person)
            if concurrence_person is not None or concurrence_person is not "NULL" :
                save_notification_users(notification_id, concurrence_person)

    def start_new_task(self, current_date, country_id):
        def notify(d, due_date, next_due_date, approval_person):
            compliance_history_id = self.save_in_compliance_history(
                int(d["unit_id"]), int(d["compliance_id"]), current_date,
                due_date, next_due_date, int(d["assignee"]),
                d["concurrence_person"], int(approval_person)
            )

            if d["document_name"] not in ["None", "", None] :
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

            if next_due_date is not None :
                notify(d, due_date, next_due_date, approval_person)
            return next_due_date, trigger_before

        # -- start_new_task

        data = self.get_compliance_to_start(current_date, country_id)
        for d in data :
            if d["division_id"] == 0 :
                d["division_id"] = "NULL"
            if d["concurrence_person"] == 0 :
                d["concurrence_person"] = "NULL"
            approval_person = int(d["approval_person"])
            if d["frequency"] == 1 :
                next_due_date = "0000-00-00"
                notify(d, d["due_date"], next_due_date, approval_person)

            else:
                next_due_date = trigger_before = None
                due_date = d["due_date"]
                next_due_date, trigger_before = start_next_due_date_task(d, due_date, approval_person)
                if next_due_date is not None :
                    while (next_due_date - timedelta(days=trigger_before)) <= current_date :
                        # start for next-due-date
                        next_due_date, trigger_before = start_next_due_date_task(d, next_due_date, approval_person)

                self.update_assign_compliance_due_date(trigger_before, next_due_date, d["unit_id"], d["compliance_id"])

    def start(self, current_date, country_id):
        print "task started"
        self.start_new_task(current_date, country_id)
