import datetime
import traceback
from server.dbase import Database
from processes.auto_start_task import KnowledgeConnect
from server import logger
from server.emailcontroller import EmailHandler
from server.common import (return_hour_minute, convert_to_dict, get_current_date)
NOTIFY_TIME = "11:52"
email = EmailHandler()
class AutoNotify(Database):
    def __init__(self, c_db_ip, c_db_username, c_db_password, c_db_name, c_db_port, client_id, current_date):
        super(AutoNotify, self).__init__(
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

    def get_client_settings(self):
        query = "SELECT assignee_reminder, escalation_reminder_in_advance, escalation_reminder \
            FROM tbl_client_groups"
        rows = self.select_all(query)
        columns = ["assignee_reminder", "escalation_reminder_in_advance", "escalation_reminder"]
        result = convert_to_dict(rows, columns)
        return result

    def get_inprogress_compliances(self):
        query = "SELECT distinct t1.compliance_history_id, t1.unit_id, t1.compliance_id, t1.start_date, \
            t1.due_date, t3.document_name, t3.compliance_task, \
            t2.assignee, t2.concurrence_person, t2.approval_person, t4.unit_code, t4.unit_name, \
            t4.business_group_id, t4.legal_entity_id, t4.division_id, t2.country_id, \
            t3.domain_id, t3.frequency_id FROM \
            tbl_compliance_history t1 INNER JOIN tbl_assigned_compliances t2 on \
            t1.compliance_id = t2.compliance_id \
            INNER JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id \
            INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id WHERE \
            IFNULL(t1.approve_status, 0) != 1 "

        rows = self.select_all(query)
        columns = [
            "compliance_history_id", "unit_id", "compliance_id", "start_date", "due_date",
            "document_name", "compliance_task", "assignee", "concurrence_person", "approval_person",
            "unit_code", "unit_name", "business_group_id", "legal_entity_id", "division_id", "country_id",
            "domain_id", "frequency_id"
        ]
        result = convert_to_dict(rows, columns)
        return result

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None :
                q = "INSERT INTO tbl_notification_user_log(notification_id, user_id)\
                    VALUES (%s, %s)"
                self.execute(q, [notification_id, user_id])

        # notification_id = get_new_id(db, "tbl_notifications_log", "notification_id")
        created_on = get_current_date()
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
        save_notification_users(notification_id, assignee)
        if notify_to_all:
            if approval_person is not None and assignee != approval_person :
                save_notification_users(notification_id, approval_person)
            if concurrence_person is not None or concurrence_person is not "NULL" :
                save_notification_users(notification_id, concurrence_person)

    def reminder_to_assignee(self, client_info, compliance_info):
        current_date = get_current_date()
        try :
            # print "begin process to remind inprogress compliance task %s " % (current_date)
            # client_info = get_client_settings(db)
            if client_info :
                reminder_interval = int(client_info[0]["assignee_reminder"])
                print reminder_interval
                count = 0
                for c in compliance_info:
                    if c["due_date"] is None :
                        continue

                    if c["due_date"].date() < current_date.date() :
                        print "skipped due_date", c["due_date"].date()
                        continue
                    days_left = abs((c["due_date"].date() - current_date.date()).days) + 1

                    if c["document_name"] not in (None, "None", "") :
                        compliance_name = c["document_name"] + " - " + c["compliance_task"]
                    else :
                        compliance_name = c["compliance_task"]
                    date_diff = abs((current_date.date() - c["start_date"].date()).days)
                    if date_diff == 0:
                        print current_date.date()
                        print c["start_date"].date()
                        print "skipped date_diff ", 0
                        continue

                    # print date_diff
                    # print (date_diff % reminder_interval)

                    notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
                    extra_details = " %s - Reminder" % (c["compliance_history_id"])
                    if (date_diff % reminder_interval) == 0 :
                        self.save_in_notification(
                            c["country_id"], c["domain_id"], c["business_group_id"], c["legal_entity_id"],
                            c["division_id"], c["unit_id"], c["compliance_id"], c["assignee"],
                            c["concurrence_person"], c["approval_person"],
                            notification_text, extra_details, notification_type_id=2, notify_to_all=False
                        )
                        a_name, assignee_email = self.get_email_id_for_users(c["assignee"])
                        email.notify_to_assignee(
                            a_name, days_left, compliance_name,
                            c["unit_name"], assignee_email
                        )
                        count += 1
                print "%s compliances remind to assignee" % (count)
        except Exception, e:
            print e
            print(traceback.format_exc())

    def reminder_before_due_date(self, client_info, compliance_info):
        current_date = get_current_date()
        print "begin process to remind inprogress compliance task to all %s " % (current_date)
        reminder_interval = int(client_info[0]["escalation_reminder_in_advance"])
        cnt = 0
        for c in compliance_info:
            if c["due_date"] is None :
                continue

            if c["document_name"] not in (None, "None", "") :
                compliance_name = c["document_name"] + " - " + c["compliance_task"]
            else :
                compliance_name = c["compliance_task"]

            if c["due_date"].date() < current_date.date() :
                print "skipped due_date", c["due_date"]
                continue

            if c["due_date"] is None :
                continue

            days_left = abs((c["due_date"].date() - current_date.date()).days) + 1
            if days_left == 0 :
                print "skipped days_left 0",
                continue

            notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
            extra_details = " %s - Reminder" % (c["compliance_history_id"])
            if days_left == reminder_interval:
                self.save_in_notification(
                    c["country_id"], c["domain_id"], c["business_group_id"],
                    c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                    c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                    extra_details, notification_type_id=2
                )
                a_name, assignee_email = self.get_email_id_for_users(c["assignee"])
                cc_person = []
                concurrence_person = c["concurrence_person"]
                if concurrence_person == 0 :
                    concurrence_person = None
                if concurrence_person is not None :
                    c_name, concurrence_email = self.get_email_id_for_users(concurrence_person)
                    cc_person.append(concurrence_email)
                ap_name, approval_email = self.get_email_id_for_users(c["approval_person"])
                cc_person.append(approval_email)
                email.notify_before_due_date(
                    a_name, days_left, compliance_name,
                    c["unit_name"],
                    assignee_email, cc_person
                )
                cnt += 1
        print "%s compliance remind before due date" % cnt

    def notify_escalation_to_all(self, client_info, compliance_info):
        current_date = get_current_date()
        print "begin process to notify escalations to all %s" % (current_date)
        escalation_interval = int(client_info[0]["escalation_reminder"])
        cnt = 0
        for c in compliance_info :
            if c["due_date"] is None :
                continue

            if c["due_date"].date() > current_date.date() :
                print "skipped due_date ", c["due_date"]
                continue

            if c["document_name"] not in (None, "None", "") :
                compliance_name = c["document_name"] + " - " + c["compliance_task"]
            else :
                compliance_name = c["compliance_task"]
            over_due_days = abs((current_date.date() - c["due_date"].date()).days) + 1
            if over_due_days == 0 :
                print "over_due_days = 0"
                continue

            notification_text = "%s overdue by %s day(s)" % (compliance_name, over_due_days)
            extra_details = " %s - Escalation" % (c["compliance_history_id"])
            if (over_due_days % escalation_interval) == 0 :
                self.save_in_notification(
                    c["country_id"], c["domain_id"], c["business_group_id"],
                    c["legal_entity_id"], c["division_id"], c["unit_id"], c["compliance_id"],
                    c["assignee"], c["concurrence_person"], c["approval_person"], notification_text,
                    extra_details, notification_type_id=3
                )
                a_name, assignee_email = self.get_email_id_for_users(c["assignee"])
                cc_person = []
                concurrence_person = c["concurrence_person"]
                if concurrence_person == 0 :
                    concurrence_person = None
                if concurrence_person is not None :
                    c_name, concurrence_email = self.get_email_id_for_users(concurrence_person)
                    cc_person.append(concurrence_email)
                ap_name, approval_email = self.get_email_id_for_users(c["approval_person"])
                cc_person.append(approval_email)
                email.notify_before_due_date(
                    a_name, over_due_days, compliance_name,
                    c["unit_name"],
                    assignee_email, cc_person
                )
                cnt += 1
        print cnt

    def notify_task_details(self):
        client_info = self.get_client_settings()
        compliance_info = self.get_inprogress_compliances()
        if compliance_info :
            self.reminder_to_assignee(client_info, compliance_info)
            self.reminder_before_due_date(client_info, compliance_info)
            self.notify_escalation_to_all(client_info, compliance_info)

    def start_process(self):
        try :
            self.begin()
            self.notify_task_details()
            self.commit()
        except Exception, e :
            print e
            print (traceback.format_exc())
            logger.logProcessError("DailyProcess", (traceback.format_exc()))
            self.rollback()
            self.close()


class NotifyProcess(KnowledgeConnect):
    def __init__(self):
        super(NotifyProcess, self).__init__()

    def begin_process(self):
        current_date = datetime.datetime.now()
        print current_date
        current_time = return_hour_minute(current_date)
        if current_time != NOTIFY_TIME :
            print current_time
            print NOTIFY_TIME
            return

        client_info = self.get_client_db_list()
        for c in client_info:
            try :
                task = AutoNotify(
                    c["database_ip"], c["database_username"],
                    c["database_password"], c["database_name"],
                    c["database_port"], c["client_id"], current_date
                )
                task.start_process()
            except Exception, e :
                print e
                logger.logProcessError("DailyProcess", e)
                logger.logProcessError("DailyProcess", (traceback.format_exc()))

def run_notify_process():
    np = NotifyProcess()
    np.begin_process()
