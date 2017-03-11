import datetime
import traceback
from processes.process_logger import logNotifyError, logNotifyInfo
from processes.process_dbase import Database
from processes.auto_start_task import KnowledgeConnect
from server.emailcontroller import EmailHandler
from server.common import (return_hour_minute, get_current_date)

NOTIFY_TIME = "18:23"
email = EmailHandler()
class AutoNotify(Database):
    def __init__(
        self, c_db_ip, c_db_username, c_db_password, c_db_name,
        c_db_port, client_id, legal_entity_id, current_date
    ):
        super(AutoNotify, self).__init__(
            c_db_ip, c_db_port, c_db_username, c_db_password, c_db_name
        )
        self.connect()
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.current_date = current_date

    def get_email_id_for_users(self, user_id):
        q = "SELECT employee_name, email_id from tbl_users where user_id = %s"
        logNotifyInfo("user_email_id", q % (user_id))
        row = self.select_one(q, [user_id])
        if row :
            return row["employee_name"], row["email_id"]
        else :
            return None, None

    def get_client_settings(self):
        query = "SELECT assignee_reminder, escalation_reminder_in_advance, escalation_reminder, reassign_service_provider, " + \
            " c.email_id " + \
            " FROM tbl_reminder_settings as r" + \
            " INNER JOIN tbl_client_groups as c on c.client_id = r.client_id " +\
            " where legal_entity_id = %s "
        logNotifyInfo("client_settings", query % (self.legal_entity_id))
        rows = self.select_one(query, [self.legal_entity_id])
        if rows :
            return rows
        else :
            return

    def get_inprogress_compliances(self):
        query = "SELECT distinct t1.compliance_history_id, t1.unit_id, t1.compliance_id, t1.start_date, " + \
            " t1.due_date, t3.document_name, t3.compliance_task, " + \
            " t2.assignee, t2.concurrence_person, t2.approval_person, t4.unit_code, t4.unit_name, " + \
            " t4.business_group_id, t4.legal_entity_id, t4.division_id, t2.country_id, " + \
            " t3.domain_id, t3.frequency_id FROM  " + \
            " tbl_compliance_history t1 INNER JOIN tbl_assign_compliances t2 on " + \
            " t1.compliance_id = t2.compliance_id " + \
            " INNER JOIN tbl_compliances t3 on t1.compliance_id = t3.compliance_id " + \
            " INNER JOIN tbl_units t4 on t1.unit_id = t4.unit_id WHERE " + \
            " IFNULL(t1.approve_status, 0) != 1 "
        logNotifyInfo("get_inprogress_compliances", query)
        rows = self.select_all(query)
        return rows

    def save_in_notification(
        self, country_id, domain_id, business_group_id, legal_entity_id, division_id,
        unit_id, compliance_id, assignee, concurrence_person, approval_person,
        notification_text, extra_details, notification_type_id, notify_to_all=True
    ):
        def save_notification_users(notification_id, user_id):
            if user_id is not "NULL" and user_id is not None :
                q = "INSERT INTO tbl_notifications_user_log(notification_id, user_id) " + \
                    " VALUES (%s, %s) "
                v = (notification_id, user_id)
                logNotifyInfo("save_notification_users", q % v)
                self.execute(q, v)

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
                # reminder_interval = int(client_info["assignee_reminder"])
                # logNotifyInfo("reminder_to_assignee", reminder_interval)
                count = 0
                for c in compliance_info:
                    if c["due_date"] is None :
                        continue

                    # if c["due_date"].date() < current_date.date() :
                    #     print "skipped due_date because due_date crossed", c["due_date"].date()
                    #     logNotifyInfo("skipped due_date", c["due_date"].date())
                    #     continue
                    days_left = abs((c["due_date"].date() - current_date.date()).days) + 1

                    if c["document_name"] not in (None, "None", "") :
                        compliance_name = c["document_name"] + " - " + c["compliance_task"]
                    else :
                        compliance_name = c["compliance_task"]
                    # date_diff = abs((current_date.date() - c["start_date"].date()).days)
                    # if date_diff == 0:
                    #     logNotifyInfo("skipped due_date reminder days is 0", current_date.date())
                    #     logNotifyInfo("skipped due_date", c["start_date"].date())
                    #     logNotifyInfo("skipped date_diff ", 0)
                    #     continue

                    # print date_diff
                    # print (date_diff % reminder_interval)

                    notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
                    extra_details = " %s - Reminder" % (c["compliance_history_id"])
                    # if (date_diff % reminder_interval) == 0 :
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

                logNotifyInfo("reminder_to_assignee ", "%s compliances remind to assignee" % (count))
        except Exception, e:
            print e
            print(traceback.format_exc())

    def reminder_before_due_date(self, client_info, compliance_info):
        current_date = get_current_date()
        logNotifyInfo("before_due_date", "begin process to remind inprogress compliance task to all %s " % (current_date))

        # reminder_interval = int(client_info["escalation_reminder_in_advance"])
        cnt = 0
        for c in compliance_info:
            if c["due_date"] is None :
                continue

            if c["document_name"] not in (None, "None", "") :
                compliance_name = c["document_name"] + " - " + c["compliance_task"]
            else :
                compliance_name = c["compliance_task"]

            # if c["due_date"].date() < current_date.date() :
            #     logNotifyInfo("skipped due_date crossed current date", c["due_date"])
            #     continue

            days_left = abs((c["due_date"].date() - current_date.date()).days) + 1

            notification_text = "%s day(s) left to complete %s task" % (days_left, compliance_name)
            extra_details = " %s - Reminder" % (c["compliance_history_id"])
            # if days_left == reminder_interval:
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
        logNotifyInfo("before_due_date", "%s compliance remind before due date" % cnt)

    def notify_escalation_to_all(self, client_info, compliance_info):
        current_date = get_current_date()
        logNotifyInfo("escalation_to_all", "begin process to notify escalations to all %s" % (current_date))
        # escalation_interval = int(client_info["escalation_reminder"])
        cnt = 0
        for c in compliance_info :
            if c["due_date"] is None :
                continue

            # if c["due_date"].date() > current_date.date() :
            #     logNotifyInfo("skipped due_date ", c["due_date"])
            #     continue

            if c["document_name"] not in (None, "None", "") :
                compliance_name = c["document_name"] + " - " + c["compliance_task"]
            else :
                compliance_name = c["compliance_task"]

            over_due_days = abs((current_date.date() - c["due_date"].date()).days) + 1

            notification_text = "%s overdue by %s day(s)" % (compliance_name, over_due_days)
            extra_details = " %s - Escalation" % (c["compliance_history_id"])
            # if (over_due_days % escalation_interval) == 0 :
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
        logNotifyInfo("escalation count", cnt)

    def get_reminder_to_assignee_compliance(self):
        q = "select ch.compliance_history_id, ch.unit_id, ch.compliance_id, ch.start_date, " + \
            "ch.due_date, c.document_name, c.compliance_task," + \
            " ch.completed_by as assignee, ch.concurred_by as concurrence_person, ch.approved_by as approval_person, " + \
            " u.unit_code, u.unit_name, u.business_group_id, u.legal_entity_id, " + \
            " u.division_id, u.country_id, c.domain_id, c.frequency_id " + \
            " from tbl_compliance_history as ch " + \
            " inner join tbl_compliances as c on ch.compliance_id = c.compliance_id " + \
            " inner join tbl_units as u on ch.unit_id = u.unit_id " + \
            " left join tbl_reminder_settings as rs on ch.legal_entity_id = rs.legal_entity_id " + \
            " Where ch.current_status < 3 and" + \
            " date(ch.due_date) > date(CONVERT_TZ(UTC_TIMESTAMP,'+00:00','+05:30')) " + \
            " AND MOD(datediff(ch.due_date,CONVERT_TZ(UTC_TIMESTAMP,'+00:00','+05:30')),rs.assignee_reminder) = 0 "

        logNotifyInfo("get_inprogress_compliances", q)
        rows = self.select_all(q)
        return rows

    def escalation_reminder_in_advance(self):
        q = "select ch.compliance_history_id, ch.unit_id, ch.compliance_id, ch.start_date, " + \
            "ch.due_date, c.document_name, c.compliance_task, " + \
            " ch.completed_by as assignee, ch.concurred_by as concurrence_person, ch.approved_by as approval_person, " + \
            " u.unit_code, u.unit_name, u.business_group_id, u.legal_entity_id, " + \
            " u.division_id, u.country_id, c.domain_id, c.frequency_id " + \
            " from tbl_compliance_history as ch " + \
            " inner join tbl_compliances as c on ch.compliance_id = c.compliance_id " + \
            " inner join tbl_units as u on ch.unit_id = u.unit_id " + \
            " left join tbl_reminder_settings as rs on ch.legal_entity_id = rs.legal_entity_id " + \
            " Where ch.current_status < 3 and" + \
            " date_sub(ch.due_date, INTERVAL rs.escalation_reminder_in_advance DAY) = date(CONVERT_TZ(UTC_TIMESTAMP,'+00:00','+05:30'));"
        logNotifyInfo("get_inprogress_compliances", q)
        rows = self.select_all(q)
        return rows

    def escalation_reminder_after_due_date(self):
        q = "select ch.compliance_history_id, ch.unit_id, ch.compliance_id, ch.start_date, " + \
            "ch.due_date, c.document_name, c.compliance_task, " + \
            "ch.completed_by as assignee, ch.concurred_by as concurrence_person, ch.approved_by as approval_person, " + \
            " u.unit_code, u.unit_name, u.business_group_id, u.legal_entity_id, " + \
            " u.division_id, u.country_id, c.domain_id, c.frequency_id " + \
            " from tbl_compliance_history as ch " + \
            " inner join tbl_compliances as c on ch.compliance_id = c.compliance_id " + \
            " inner join tbl_units as u on ch.unit_id = u.unit_id " + \
            " left join tbl_reminder_settings as rs on ch.legal_entity_id = rs.legal_entity_id " + \
            " Where ch.current_status < 3 and" + \
            " date(ch.due_date) < date(CONVERT_TZ(UTC_TIMESTAMP,'+00:00','+05:30')) " + \
            " AND MOD(datediff(CONVERT_TZ(UTC_TIMESTAMP,'+00:00','+05:30'),ch.due_date),rs.escalation_reminder) = 0 "

        logNotifyInfo("get_inprogress_compliances", q)
        rows = self.select_all(q)
        return rows

    def notify_task_details(self):
        client_info = self.get_client_settings()

        self.reminder_to_assignee(client_info, self.get_reminder_to_assignee_compliance())
        self.reminder_before_due_date(client_info, self.escalation_reminder_in_advance())
        self.notify_escalation_to_all(client_info, self.escalation_reminder_after_due_date())

    # for service providers
    def get_compliance_count_to_reassign(self):
        q = "select count(compliance_history_id), t2.service_provider_id, t3.service_provider_name, t3.short_name, t3.blocked_on from tbl_compliance_history as t1 " + \
            " inner join tbl_users as t2 on t1.completed_by = t2.user_id and t2.is_service_provider = 1 " + \
            " inner join tbl_service_providers as t3 on t2.service_provider_id = t3.service_provider_id and t3.is_blocked = 1  " + \
            " group by t2.service_provider_id "
        rows = self.select_all(q)
        return rows

    def notify_compliance_to_reassign(self):
        current_date = get_current_date()
        client_info = self.get_client_settings()
        groupadmin_email = client_info.get("email_id")
        service_provider_reminder = client_info.get("reassign_service_provider")

        service_info = self.get_compliance_count_to_reassign()
        for r in service_info :
            sname = "%s - %s" % (r["short_name"], r["service_provider_name"])
            bdate = r["blocked_on"]
            if bdate is None :
                continue
            if bdate > current_date :
                continue
            if abs((current_date.date() - bdate.date()).days) == service_provider_reminder :
                email.notify_group_admin_toreassign_sp_compliances(sname, groupadmin_email)

    def start_process(self):
        try :
            self.begin()
            self.notify_task_details()
            self.notify_compliance_to_reassign()
            self.commit()
            self.close()
        except Exception, e :
            print e
            print (traceback.format_exc())
            logNotifyError("start_process", (traceback.format_exc()))
            self.rollback()
            self.close()


class NotifyProcess(KnowledgeConnect):
    def __init__(self):
        super(NotifyProcess, self).__init__()

    def begin_process(self):
        current_date = datetime.datetime.now()
        logNotifyInfo("current_date", current_date)
        current_time = return_hour_minute(current_date)
        if current_time != NOTIFY_TIME :
            logNotifyInfo("current_time", current_time)
            logNotifyInfo("NOTIFY_TIME", NOTIFY_TIME)
            return

        client_info = self.get_client_db_list()
        print client_info
        for c in client_info:
            try :
                print c
                task = AutoNotify(
                    c["database_ip"], c["database_username"],
                    c["database_password"], c["database_name"],
                    c["database_port"], c["client_id"], c["legal_entity_id"],
                    current_date
                )
                task.start_process()
            except Exception, e :
                print e
                logNotifyError("DailyProcess", e)
                logNotifyError("DailyProcess", (traceback.format_exc()))

def run_notify_process():
    np = NotifyProcess()
    np.begin_process()
