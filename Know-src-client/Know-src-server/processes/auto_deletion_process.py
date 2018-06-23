#!/usr/bin/python

import datetime
from dateutil import relativedelta
import traceback

from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from server.countrytimestamp import countries
from server.emailcontroller import EmailHandler
from server.common import (
    time_convertion, return_date,
)

from processes.auto_start_task import KnowledgeConnect
from processes.process_dbase import Database
from processes.process_logger import logProcessError, logProcessInfo

from server.constants import (
    CLIENT_URL
)

mysqlHost = KNOWLEDGE_DB_HOST
mysqlUser = KNOWLEDGE_DB_USERNAME
mysqlPassword = KNOWLEDGE_DB_PASSWORD
mysqlDatabase = KNOWLEDGE_DATABASE_NAME
mysqlPort = KNOWLEDGE_DB_PORT

seven_years_before_data_download_path = "/seven_years_before_data/download/"
seven_years_before_data_folder_path = "./seven_years_before_data/"

email = EmailHandler()


class AutoDeletionStart(Database):
    def __init__(
        self, c_db_ip, c_db_username, c_db_password, c_db_name, c_db_port,
        client_id, legal_entity_id, current_date,
        country_id
    ):
        super(AutoDeletionStart, self).__init__(
            c_db_ip, c_db_port, c_db_username, c_db_password, c_db_name
        )
        self._c_db_ip = c_db_ip
        self._c_db_name = c_db_name
        self.connect()
        self.client_id = client_id
        self.legal_entity_id = legal_entity_id
        self.current_date = current_date
        self.country_id = country_id

    def get_new_id(self, table_name, column_name):
        query = "SELECT MAX(%s)+1 as msx_id FROM %s" % (column_name, table_name)
        row = self.select_one(query)
        if row.get("msx_id") is None :
            return 1
        return row.get("msx_id")

    def get_configuration_for_client_country(self):
        query = "SELECT domain_id, month_from FROM tbl_client_configuration " + \
            "WHERE country_id = %s"
        rows = self.select_all(query, [self.country_id])
        return rows

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

    def delete_data(self, domain_id):
        deletion_year = 7
        query = "DELETE FROM tbl_compliance_history WHERE  compliance_id in ( " + \
            " SELECT count(0) FROM tbl_compliance_history as t1 " + \
            "INNER JOIN tbl_client_compliances as t2 on t1.unit_id = t2.unit_id and " + \
            " t1.compliance_id = t2.compliance_id " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " WHERE (t1.validity_date < DATE_SUB(now(), INTERVAL %s YEAR) or " + \
            " t1.validity_date = 0 or t1.validity_date is null) and t1.due_date < DATE_SUB(now(), INTERVAL %s YEAR) " + \
            " and t2.domain_id = %s and t3.country_id = %s )"

        print query % (deletion_year, deletion_year, domain_id, self.country_id)

        # self.execute(query, [deletion_year, deletion_year, domain_id, self.country_id])

    def is_seven_years_before_data_available(self, domain_id):
        deletion_year = 7

        query = "SELECT count(0) cnt FROM tbl_compliance_history as t1 " + \
            "INNER JOIN tbl_client_compliances as t2 on t1.unit_id = t2.unit_id and " + \
            " t1.compliance_id = t2.compliance_id " + \
            " inner join tbl_units as t3 on t1.unit_id = t3.unit_id " + \
            " WHERE (t1.validity_date < DATE_SUB(now(), INTERVAL %s YEAR) or " + \
            " t1.validity_date = 0 or t1.validity_date is null) and t1.due_date < DATE_SUB(now(), INTERVAL %s YEAR) " + \
            " and t2.domain_id = %s and t3.country_id = %s "

        print query % (deletion_year, deletion_year, domain_id, self.country_id)

        result = self.select_one(query, [deletion_year, deletion_year, domain_id, self.country_id])
        if result :
            print result
            if result.get("cnt") > 0:
                return True
            else:
                return False
        else:
            return False

    def generate_seven_years_before_report(self, domain_id, country_id):
        query_columns = "c.compliance_task as compliance_name, c.document_name, " + \
            " c.compliance_description as description, " + \
            " ch.start_date, ch.due_date, ch.completion_date, " + \
            " ch.validity_date, ch.remarks, ch.completed_on, " + \
            " ch.concurred_on, ch.approved_on, " + \
            " (SELECT concat(unit_code, '-', unit_name) " + \
            " FROM tbl_units un WHERE un.unit_id = ch.unit_id) as unit_name, " + \
            " (SELECT concat(employee_code, '-', employee_name) " + \
            " FROM tbl_users us WHERE us.user_id = ch.completed_by) as assignee, " + \
            " (SELECT concat(employee_code, '-', employee_name) " + \
            " FROM tbl_users us WHERE us.user_id = ch.concurred_by) as concurrence_person, " + \
            " (SELECT concat(employee_code, '-', employee_name) " + \
            " FROM tbl_users us WHERE us.user_id = ch.approved_by) as approval_person, " + \
            " ch.documents"
        query = "SELECT " + query_columns + " FROM tbl_compliance_history ch " + \
            " INNER JOIN tbl_compliances c ON " + \
            " (c.compliance_id = ch.compliance_id) " + \
            " WHERE  c.compliance_id in ( " + \
            " SELECT compliance_id FROM tbl_client_compliances " + \
            " WHERE client_statutory_id in( " + \
            " SELECT client_statutory_id FROM tbl_client_statutories " + \
            " WHERE country_id = '%s' " + \
            " AND domain_id = '%s')) AND (validity_date < DATE_SUB( " + \
            " now(), INTERVAL 7 YEAR) " + \
            " or validity_date = 0 or validity_date is null) " + \
            " AND due_date <  " + \
            " DATE_SUB(now(), INTERVAL 7 YEAR)"

        results = self.select_all(query, [country_id, domain_id])

        # Paths
        self.folder_path = "./seven_years_before_data/%s/" % str(
            self.client_id)
        self.excel_file_path = "%sComplianceDetails.xlsx" % (
            self.folder_path)
        documents = self.generateExcelFile(
            results, self.folder_path, self.excel_file_path
        )
        zip_file_path = "./seven_years_before_data/%s/documents" % str(
            self.client_id)
        zip_file_name = self.generateZipFile(
            zip_file_path, "seven_years_before_data", documents
        )
        download_link = "%sdownload_7_year_data/bkup/%s/%s" % (
            CLIENT_URL, self.client_id, zip_file_name
        )
        return download_link

    def bundle_seven_years_before_data(self, domain_id):
        download_link = self.generate_seven_years_before_report(
            self.country_id, domain_id
        )
        return download_link

    def is_already_notified(
        self, notification_text, extra_details
    ):
        query = "SELECT count(*) as cnt FROM tbl_notifications_log WHERE notification_text = %s and extra_details = %s"
        rows = self.select_one(query, [notification_text, extra_details])
        if rows.get("cnt") > 0:
            return True
        else:
            return False

    def notify_client_regarding_auto_deletion(
        self, download_link, domain_id, deletion_date
    ):

        query = "SELECT group_name FROM tbl_client_groups where client_id = %s"
        rows = self.select_one(query, [self.client_id])
        group_name = rows.get("group_name")

        query = "SELECT country_name FROM tbl_countries WHERE country_id = %s"
        rows = self.select_one(query, [self.country_id])
        country_name = rows.get("country_name")

        query = "SELECT domain_name FROM tbl_domains WHERE domain_id = %s"
        rows = self.select_one(query, [domain_id])
        domain_name = rows.get("domain_name")

        notification_text = '''Dear Client Admin,  \
        Your data and documents before 7 years for %s in the country %s and domain %s \
        will be deleted on %s. Before deletion you can download all the data <a href="%s">here </a> ''' % (
            group_name, country_name, domain_name, deletion_date.date(), download_link
        )
        extra_details = "0 - Auto Deletion"

        if not self.is_already_notified(notification_text, extra_details):
            notification_id = self.get_new_id("tbl_notifications_log", "notification_id")
            created_on = datetime.datetime.now()
            query = "INSERT INTO tbl_notifications_log " + \
                " (notification_id, notification_type_id, " + \
                " notification_text, extra_details, created_on " + \
                " ) VALUES (%s, %s, '%s', '%s', '%s')"
            self.execute(query, [notification_id, 1, notification_text, extra_details, created_on])

            q = "INSERT INTO tbl_notification_user_log(notification_id, user_id) " + \
                " VALUES (%s, %s)"

            self.execute(q, [notification_id, 0])

            q = "SELECT email_id from tbl_users where user_category_id = 1 and is_active = 1 "
            rows = self.select_one(q)
            admin_mail_id = rows.get("email_id")
            email.notify_auto_deletion(
                admin_mail_id, notification_text
            )

    def delete_seven_years_before_data(self):
        domain_wise_config = self.get_configuration_for_client_country()
        domains_to_be_notified = []
        for config in domain_wise_config:
            domain_id = config["domain_id"]
            period_from = config["month_from"]
            print period_from
            if self.is_new_year_starting_within_30_days(
                period_from
            ):
                print " new year about to start"
                if self.is_current_date_is_deletion_date(
                    period_from
                ):
                    print "before data delete"
                    self.delete_data(domain_id)
                elif self.is_seven_years_before_data_available(domain_id):
                    domains_to_be_notified.append(domain_id)
                    download_link = self.bundle_seven_years_before_data(domain_id)
                    deletion_date = datetime.datetime(self.current_date.year, period_from, 1)
                    if deletion_date.date() < self.current_date:
                        deletion_date = datetime.datetime(self.current_date.year + 1, period_from, 1)
                    self.notify_client_regarding_auto_deletion(
                       download_link, domain_id, deletion_date
                    )

    def run_deletion_process(self):
        self.delete_seven_years_before_data()

    def start_process(self):
        if self._connection is None :
            details = "%s, %s" % (self._c_db_ip, self._c_db_name)
            logProcessInfo("connection not found %s" % self.client_id, details)
            return
        try:
            self.begin()
            self.run_deletion_process()
            self.commit()
        except Exception, e:
            logProcessError("start_deletion_process %s" % self.client_id, str(e))
            logProcessError("start_deletion_process", str(traceback.format_exc()))
            logProcessError("start_deletion_process", (traceback.format_exc()))
            print e

class DeletionProcess(KnowledgeConnect):
    def __init__(self):
        super(DeletionProcess, self).__init__()

    def begin_process(self):
        logProcessInfo("AutoDeletionProcess", "Process Begin")
        country_time_zones = sorted(countries)
        country_list = self.get_countries()
        print country_list
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
                print "country --", c["country_name"]
                country_id = c["country_id"]
                print current_date
                client_info = self.get_client_db_list()
                logProcessInfo("AutoDeletionProcess", "Process Begin")
                for ci in client_info :
                    print ci["client_id"]
                    try :
                        delp = AutoDeletionStart(
                            ci["database_ip"],
                            ci["database_username"],
                            ci["database_password"],
                            ci["database_name"], ci["database_port"],
                            ci["client_id"], ci["legal_entity_id"],
                            current_date, country_id
                        )
                        delp.start_process()
                    except Exception, e :
                        logProcessError("AutoDeletionProcess", e)
                        logProcessError("AutoDeletionProcess", (traceback.format_exc()))


def run_deletion_proess():
    delp = DeletionProcess()
    delp.begin_process()
