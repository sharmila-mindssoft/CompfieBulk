import os
import json
import collections
import mysql.connector
import requests
import threading
from requests.exceptions import ConnectionError
from datetime import datetime, timedelta
from server.dbase import Database
from server.common import get_date_time
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME)
from bulkupload.client_bulkconstants import (
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH, CLIENT_TEMP_FILE_SERVER,
    BULK_UPLOAD_DB_USERNAME, BULK_UPLOAD_DB_PASSWORD,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DATABASE_NAME, BULK_UPLOAD_DB_PORT)
from ..buapiprotocol.pastdatadownloadbulk import (
    calculate_final_due_dates, return_past_due_dates)
from client_keyvalidationsettings import (
    csv_params, parse_csv_dictionary_values)
from ..client_bulkuploadcommon import (
    write_data_to_excel, rename_file_type)


__all__ = [
    "ValidateCompletedTaskCurrentYearCsvData",
    "ValidateCompletedTaskForSubmit"
]
################################
'''
    SourceDB : This class methods executed with main db connection
    also check csv data validation
'''
################################


class SourceDB(object):
    def __init__(self):
        self._source_db = None
        self._source_db_con = None
        self._knowledge_db = None
        self._knowledge_db_con = None
        # self.Client_Group = {}
        self.legal_entity = {}
        self.domain = {}
        self.unit_code = {}
        self.unit_name = {}
        self.statutories = {}
        self.compliance_task = {}
        self.compliance_description = {}
        self.compliance_frequency = {}
        self.assignee = {}
        # self.connect_source_db()
        self._validation_method_maps = {}
        self.status_check_methods()
        self._csv_column_name = []
        self.csv_column_fields()
        self._doc_names = []
        self._past_due_dates = {}
        self.trigger_before_days = {}
        self.frequency_id_name_map = {}
        self.hierarchy_checker = {}
        self.stop = True
        # self.get_doc_names()

    def connect_source_db(self, legal_entity_id):
        self._knowledge_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False
        )

        self._knowledge_db = Database(self._knowledge_db_con)
        self._knowledge_db.begin()

        query = "select t1.client_database_id, t1.database_name, " + \
            "t1.database_username, t1.database_password, " + \
            "t3.database_ip, database_port " + \
            " from tbl_client_database_info as t1 " + \
            " inner join tbl_client_database as t2 on " + \
            " t2.client_database_id = t1.client_database_id " + \
            " inner join tbl_database_server as t3 on " + \
            " t3.database_server_id = t2.database_server_id " + \
            " where t1.db_owner_id = %s and t1.is_group = 0;"
        param = [legal_entity_id]

        result = self._knowledge_db.select_all(query, param)

        if len(result) > 0:
            for row in result:
                dhost = row["database_ip"]
                uname = row["database_username"]
                pwd = row["database_password"]
                port = row["database_port"]
                db_name = row["database_name"]

                self._source_db_con = mysql.connector.connect(
                    user=uname,
                    password=pwd,
                    host=dhost,
                    database=db_name,
                    port=port,
                    autocommit=False,
                )
        self._source_db = Database(self._source_db_con)
        self._source_db.begin()

    def close_source_db(self):
        self._source_db.close()
        self.__source_db_con.close()

    def init_values(self, legal_entity_id):
        self.connect_source_db(legal_entity_id)
        self.get_legal_entities()
        self.get_domains()
        self.get_unit_code()
        self.get_unit_name()
        self.get_primary_legislation()
        self.get_secondary_legislation()
        self.get_compliance_task()
        self.get_compliance_description()
        self.get_compliance_frequency()
        self.get_assignee()
        self.generate_hierarchy_checker()

    def get_legal_entities(self):
        query = "SELECT legal_entity_id, legal_entity_name, " + \
            "is_closed FROM tbl_legal_entities;"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.legal_entity[d["legal_entity_name"]] = d

    def get_domains(self):
        query = "SELECT domain_id, domain_name, is_active  FROM tbl_domains"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.domain[d["domain_name"]] = d

    def get_unit_code(self):
        query = "SELECT unit_id, client_id, legal_entity_id, " + \
            "unit_code, unit_name, is_closed, country_id FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.unit_code[d["unit_code"]] = d

    def return_unit_domain_id(self, domain_name, unit_code):
        domain_id = None
        unit_id = None
        try:
            domain_id = self.domain[domain_name]["domain_id"]
            unit_id = self.unit_code[unit_code]["unit_id"]
        except KeyError:
            pass
        return unit_id, domain_id

    def get_unit_name(self):
        query = "SELECT unit_id, client_id, legal_entity_id, " + \
            "unit_code, unit_name, is_closed FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.unit_name[d["unit_name"]] = d

    def get_primary_legislation(self):
        query = "Select SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING(" + \
            " SUBSTRING(" + \
            " t.statutory_mapping,3),1, CHAR_LENGTH(t.statutory_mapping) " + \
            " -4), '>>', 1),'\",',1) AS primary_legislation, domain_id, " + \
            " country_id from " + \
            " tbl_compliances t where is_active = 1"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.statutories[d["primary_legislation"]] = d

    def get_secondary_legislation(self):
        query = "Select SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING(" + \
            " SUBSTRING(" + \
            " t.statutory_mapping,3),1, CHAR_LENGTH(t.statutory_mapping) " + \
            " -4), '>>', 1),'\",',1) AS primary_legislation, " + \
            " TRIM(SUBSTRING_INDEX(SUBSTRING(SUBSTRING( " + \
            " SUBSTRING_INDEX(SUBSTRING(SUBSTRING(statutory_mapping,3 " + \
            " ),1,CHAR_LENGTH(statutory_mapping) -4),'>>',2), " + \
            " CHAR_LENGTH(SUBSTRING_INDEX(SUBSTRING(SUBSTRING( " + \
            " statutory_mapping,3),1, CHAR_LENGTH(statutory_mapping) " + \
            " -4), '>>', 1))+1),3),'\",',1)) AS secondary_legislation " + \
            " from tbl_compliances t where is_active = 1"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.statutories[d["secondary_legislation"]] = d

    def get_compliance_task(self):
        query = "SELECT compliance_id, statutory_provision, " + \
            "case when ifnull(document_name,'') = '' then " + \
            "trim(compliance_task) else trim(Concat_ws( " + \
            "' - ',document_name, compliance_task)) end AS " + \
            " compliance_task, compliance_description, " + \
            "is_active, frequency_id from tbl_compliances t1"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.compliance_task[d["compliance_task"]] = d

    def get_compliance_description(self):
        query = "SELECT compliance_id, statutory_provision, " + \
            " compliance_task, compliance_description, is_active " + \
            "from tbl_compliances"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.compliance_description[d["compliance_description"]] = d

    def generate_hierarchy_checker(self):
        query = "Select SUBSTRING_INDEX(SUBSTRING_INDEX(SUBSTRING(" + \
            " SUBSTRING(" + \
            " t.statutory_mapping,3),1, CHAR_LENGTH(t.statutory_mapping) " + \
            " -4), '>>', 1),'\",',1) AS primary_legislation, " + \
            " TRIM(SUBSTRING_INDEX(SUBSTRING(SUBSTRING( " + \
            " SUBSTRING_INDEX(SUBSTRING(SUBSTRING(statutory_mapping,3 " + \
            " ),1,CHAR_LENGTH(statutory_mapping) -4),'>>',2), " + \
            " CHAR_LENGTH(SUBSTRING_INDEX(SUBSTRING(SUBSTRING( " + \
            " statutory_mapping,3),1, CHAR_LENGTH(statutory_mapping) " + \
            " -4), '>>', 1))+1),3),'\",',1)) AS secondary_legislation, " + \
            " compliance_id, compliance_task, compliance_description, " + \
            " is_active from tbl_compliances t "
        rows = self._source_db.select_all(query)
        for d in rows:
            primary = d["primary_legislation"].strip()
            secondary = d["secondary_legislation"]
            compliance = d["compliance_task"]
            compliance_id = d["compliance_id"]
            description = d["compliance_description"]
            if secondary == "":
                secondary = "empty"
            else:
                secondary = secondary.strip()
            if primary not in self.hierarchy_checker:
                self.hierarchy_checker[primary] = {}
            if secondary not in self.hierarchy_checker[primary]:
                self.hierarchy_checker[primary][secondary] = {}
            if compliance not in self.hierarchy_checker[primary][secondary]:
                self.hierarchy_checker[
                    primary][secondary][compliance] = {
                        "compliance_id": compliance_id,
                        "desc": description}

    def get_compliance_frequency(self):
        query = "select frequency_id, frequency " + \
            " from tbl_compliance_frequency " + \
                " where frequency_id in (2,3)"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.compliance_frequency[d["frequency"]] = d
            self.frequency_id_name_map[d["frequency_id"]] = d["frequency"]

    def get_assignee(self):
        query = "SELECT Distinct assignee as ID, employee_code," + \
                " employee_name, " + \
                " CONCAT_WS(' - ', employee_code, employee_name) " + \
                " As Assignee " + \
                " FROM tbl_assign_compliances ac INNER JOIN " + \
                " tbl_users u ON (ac.assignee = u.user_id)"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.assignee[d["Assignee"]] = d

    def check_base(self, check_status, store, key_name, status_name):
        data = store.get(key_name)
        if data is None:
            return "Not found"

        if check_status is True:
            if status_name is None:
                if data.get("is_active") == 0:
                    return "Status Inactive"
            elif status_name == "is_closed":
                if data.get("is_closed") == 0:
                    return "Status Inactive"

        return True

    def get_past_due_dates(self, domain_id, unit_id, compliance_id):
        def generate_past_due_dates(domain_id, unit_id, compliance_id):
            rows = return_past_due_dates(
                self._source_db, domain_id, unit_id, None, compliance_id
            )
            result, summary = calculate_final_due_dates(
                self._source_db, rows, domain_id, unit_id
            )
            if domain_id not in self._past_due_dates:
                self._past_due_dates[domain_id] = {}
            if unit_id not in self._past_due_dates[domain_id]:
                self._past_due_dates[domain_id][unit_id] = {}
            if compliance_id not in self._past_due_dates[domain_id][unit_id]:
                self._past_due_dates[
                    domain_id][unit_id][compliance_id] = result
            return result
        if domain_id in self._past_due_dates:
            if unit_id in self._past_due_dates[domain_id]:
                if compliance_id in self._past_due_dates[domain_id][unit_id]:
                    return self._past_due_dates[
                        domain_id][unit_id][compliance_id]
                else:
                    return generate_past_due_dates(
                        domain_id, unit_id, compliance_id)
            else:
                return generate_past_due_dates(
                    domain_id, unit_id, compliance_id)
        else:
            return generate_past_due_dates(domain_id, unit_id, compliance_id)

    def get_trigger_before_days(self, unit_id, domain_id, compliance_id):
        def generate_trigger_before_days(unit_id, domain_id, compliance_id):
            q = "SELECT statutory_dates from tbl_assign_compliances " + \
                " where unit_id = %s  and domain_id = %s" + \
                " and compliance_id = %s"
            params = [unit_id, domain_id, compliance_id]
            rows = self._source_db.select_all(q, params)
            trigger_before_days = 0
            if rows:
                statutory_dates = rows[0]["statutory_dates"]
                statutory_dates_array = json.loads(statutory_dates)
                trigger_before_days = int(
                    statutory_dates_array[0]["trigger_before_days"])
                if domain_id not in self.trigger_before_days:
                    self.trigger_before_days[domain_id] = {}
                elif unit_id not in self.trigger_before_days[domain_id]:
                    self.trigger_before_days[domain_id][unit_id] = {}
                elif (compliance_id not in
                        self.trigger_before_days[domain_id][unit_id]):
                    self.trigger_before_days[
                        domain_id][unit_id][
                        compliance_id] = trigger_before_days
                else:
                    self.trigger_before_days[
                        domain_id][unit_id][
                        compliance_id] = trigger_before_days
            return trigger_before_days
        if domain_id in self.trigger_before_days:
            if unit_id in self.trigger_before_days[domain_id]:
                if compliance_id in self.trigger_before_days[
                        domain_id][unit_id]:
                        return self.trigger_before_days[domain_id][unit_id][
                            compliance_id]
                else:
                    return generate_trigger_before_days(
                        unit_id, domain_id, compliance_id)
            else:
                return generate_trigger_before_days(
                    unit_id, domain_id, compliance_id)
        else:
            return generate_trigger_before_days(
                unit_id, domain_id, compliance_id)

    def check_due_date(
        self, due_date, domain_name, unit_code, compliance_task,
        primary_legislation, secondary_legislation, description
    ):
        (unit_id, domain_id) = self.return_unit_domain_id(
            domain_name, unit_code)
        compliance_id = None
        compliance_task_name = self.get_compliance_task_name(compliance_task)
        secondary = secondary_legislation
        if secondary_legislation == "":
            secondary = "empty"
        try:
            data = self.hierarchy_checker[primary_legislation][
                secondary][compliance_task_name]
            if data["desc"] == description:
                compliance_id = data["compliance_id"]
        except KeyError:
            return
        if unit_id is None or domain_id is None or compliance_id is None:
            return
        due_dates = self.get_past_due_dates(domain_id, unit_id, compliance_id)
        if due_dates is None:
            return "Not Found"
        try:
            due_date = datetime.strptime(due_date, "%d-%b-%Y")
            due_date = due_date.date().strftime("%Y-%m-%d")
        except ValueError:
            return
        q = "SELECT bulk_past_data_id FROM tbl_bulk_past_data " + \
            "WHERE unit_code=%s and perimary_legislation=%s and " + \
            "secondary_legislation=%s and compliance_task_name=%s and " + \
            "compliance_description=%s and date(due_date)=%s"
        params = [
            unit_code, primary_legislation, secondary_legislation,
            compliance_task, description, due_date
        ]
        db = bulkupload_db_connect()
        _db_check = Database(db)
        try:
            _db_check.begin()
            rows = _db_check.select_all(q, params)
            if rows:
                return "Duplicate due date"
        except Exception:
            _db_check.rollback()
        if due_date in due_dates:
            return True
        else:
            return "Not Found"

    def check_is_valid_frequency(
        self, compliance_task, frequency
    ):
        try:
            frequency_id = self.compliance_task[
                compliance_task]["frequency_id"]
        except KeyError:
            return True
        orig_freq = self.frequency_id_name_map[frequency_id]
        if frequency != orig_freq:
            return "Invalid"
        else:
            return True

    def check_completion_date(
        self, unit_code, due_date, compliance_task, domain_name,
        completion_date
    ):
        (unit_id, domain_id) = self.return_unit_domain_id(
            domain_name, unit_code)
        try:
            compliance_id = self.compliance_task[
                compliance_task]["compliance_id"]
        except KeyError:
            return
        if unit_id is None or domain_id is None:
            return
        trigger_before_days = self.get_trigger_before_days(
            unit_id, domain_id, compliance_id
        )
        try:
            due_date = datetime.strptime(due_date, "%d-%b-%Y")
            completion_date = datetime.strptime(
                completion_date, "%d-%b-%Y").date()
        except ValueError:
            return
        start_date = due_date.date() - timedelta(days=trigger_before_days)
        if completion_date < start_date:
            return "Should be greater than Start Date"
        else:
            return True

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(
            True, self.legal_entity, legal_entity_name, None
        )

    def check_domain(self, domain_name):
        return self.check_base(True, self.domain, domain_name, None)

    def check_valid_unit_code(self, unit_code, unit_name):
        try:
            org_unit_name = self.unit_code[unit_code]["unit_name"]
        except KeyError:
            return "invalid"
        if org_unit_name == unit_name:
            return True
        else:
            return "Invalid"

    def check_unit_code(self, unit_code, unit_name):
        status1 = self.check_valid_unit_code(unit_code, unit_name)
        status2 = self.check_base(True, self.unit_code, unit_code, None)
        if status1 is True:
            return status2
        else:
            return status1

    def check_unit_name(self, unit_name):
        return self.check_base(True, self.unit_name, unit_name, None)

    def check_is_valid_primary_legislation(
        self, unit_code, primary_legislation
    ):
        try:
            unit_id = self.unit_code[unit_code]["unit_id"]
            unit_country_id = self.unit_code[unit_code]["country_id"]
        except KeyError:
            return
        query = "SELECT domain_id from tbl_units_organizations " + \
            " where unit_id = %s"
        params = [unit_id]
        rows = self._source_db.select_all(query, params)
        unit_domain_ids = []
        for row in rows:
            unit_domain_ids.append(row["domain_id"])
        primary_country = self.statutories[primary_legislation]["country_id"]
        primary_domain = self.statutories[primary_legislation]["domain_id"]
        if primary_country == unit_country_id:
            if primary_domain in unit_domain_ids:
                return True
        return "Not Found"

    def check_primary_legislation(self, statutories, unit_code):
        status1 = self.check_base(False, self.statutories, statutories, None)
        if status1 is True:
            return self.check_is_valid_primary_legislation(
                unit_code, statutories)
        else:
            return status1

    def check_secondary_legislation(self, statutories, primary):
        status1 = True
        try:
            if statutories not in self.hierarchy_checker[primary]:
                status1 = "Not Found"
        except KeyError:
            return
        status2 = self.check_base(False, self.statutories, statutories, None)
        if status1 is True:
            return status2
        else:
            return status1

    def check_compliance_task(self, compliance_task, primary, secondary):
        status1 = True
        compliance_task_name = self.get_compliance_task_name(compliance_task)
        try:
            if secondary == "":
                secondary = "empty"
            if (
                compliance_task_name not in self.hierarchy_checker[
                    primary][secondary]):
                status1 = "Not Found"
        except KeyError:
            return
        status2 = self.check_base(
            True, self.compliance_task, compliance_task, None)
        if status1 is True:
            return status2
        else:
            return status1

    def check_compliance_description(
        self, compliance_description, primary, secondary, compliance_task
    ):
        status1 = True
        compliance_task_name = self.get_compliance_task_name(
            compliance_task)
        try:
            if secondary == "":
                secondary = "empty"
            if (
                self.hierarchy_checker[
                    primary][secondary][compliance_task_name]["desc"] !=
                compliance_description
            ):
                status1 = "Not Found"
        except KeyError:
            return
        status2 = self.check_base(
            True, self.compliance_description, compliance_description, None)
        if status1 is True:
            return status2
        else:
            return status1

    def check_frequency(
        self, compliance_task, frequency
    ):
        status1 = self.check_is_valid_frequency(
            compliance_task, frequency
        )
        status2 = self.check_base(
            False, self.compliance_frequency, frequency, None)
        if status1 is True:
            return status2
        else:
            return status1

    def check_assignee(self, assignee):
        return self.check_base(False, self.assignee, assignee, None)

    def is_two_levels_of_approval(self, _source_db):
        query = "SELECT two_levels_of_approval FROM tbl_reminder_settings"
        rows = _source_db.select_all(query)
        return bool(rows[0]["two_levels_of_approval"])

    def get_compliance_task_name(self, compliance_task_name_data):
        compliance_task_name_check = compliance_task_name_data.split(" - ")
        compliance_task_name = compliance_task_name_check[0]
        if len(compliance_task_name_check) > 1:
            compliance_task_name = ""
            for i, x in enumerate(compliance_task_name_check):
                if i > 1:
                    compliance_task_name += " - "
                if i == 0:
                    pass
                else:
                    compliance_task_name += compliance_task_name_check[i]
        return compliance_task_name

    def save_completed_task_data(self, db, data, legal_entity_id, csv_id):
        for idx, d in enumerate(data):
            self.connect_source_db(legal_entity_id)
            columns = [
                "legal_entity_id", "unit_id", "compliance_id", "start_date",
                "due_date", "completion_date", "completed_by",
                "completed_on",
                "approve_status", "approved_by", "approved_on",
                "current_status"
            ]

            # Compliance ID
            compliance_task_name = self.get_compliance_task_name(
                d["compliance_task_name"])
            c_name = [
                compliance_task_name,
                d["compliance_description"],
                d["compliance_frequency"]
            ]
            q = "SELECT compliance_id FROM tbl_compliances where " + \
                "compliance_task = TRIM(%s) and compliance_description = " + \
                "TRIM(%s) and frequency_id = (SELECT frequency_id from " + \
                " tbl_compliance_frequency WHERE frequency=TRIM(%s))"
            compliance_id = self._source_db.select_all(q, c_name)
            # if len(compliance_id) > 0:
            compliance_id = compliance_id[0]["compliance_id"]

            completion_date = d["completion_date"]

            # Unit ID
            unit_code = [d["unit_code"]]
            q = "select unit_id from tbl_units where unit_code = TRIM(%s)"
            unit_id = self._source_db.select_all(q, unit_code)
            unit_id = unit_id[0]["unit_id"]

            # assignee_id
            assignee = [d["assignee"]]
            q = " SELECT distinct ac.assignee as ID, u.employee_code, " + \
                " u.employee_name, " + \
                " CONCAT_WS(' - ', u.employee_code, " + \
                " u.employee_name) As Assignee " + \
                " FROM tbl_assign_compliances ac INNER JOIN tbl_users u " + \
                " ON (ac.assignee = u.user_id) where " + \
                " CONCAT_WS(' - ', u.employee_code, u.employee_name)=TRIM(%s)"
            assignee_id = self._source_db.select_all(q, assignee)
            assignee_id = assignee_id[0]["ID"]

            query = "SELECT two_levels_of_approval FROM tbl_reminder_settings"
            rows = self._source_db.select_all(query)
            if int(rows[0]["two_levels_of_approval"]) == 1:
                is_two_level = True
            else:
                is_two_level = False

            # Getting Approval and Concurrence Persons
            concur_approve_columns = "approval_person, country_id, domain_id"
            if is_two_level:
                concur_approve_columns += ", concurrence_person"
            condition = "compliance_id = %s and unit_id = %s "
            tbl_assign_compliances = "tbl_assign_compliances"
            rows = self._source_db.get_data(
                tbl_assign_compliances,
                concur_approve_columns,
                condition, [compliance_id, unit_id]
            )
            concurred_by = 0
            approved_by = 0
            if len(rows) > 0:
                approved_by = rows[0]["approval_person"]
                users = [assignee_id, approved_by]
                if is_two_level:
                    concurred_by = rows[0]["concurrence_person"]
                    users.append(concurred_by)

            values = [
                legal_entity_id, unit_id, compliance_id, get_date_time(),
                d["due_date"], completion_date,
                assignee_id, completion_date,
                1, approved_by, completion_date, 3]

            if d["document_name"] != "":
                columns.append("documents")
                values.append(d["document_name"])

            if is_two_level:
                columns.append("concurrence_status")
                columns.append("concurred_by")
                columns.append("concurred_on")
                values.append(1)
                values.append(concurred_by)
                values.append(completion_date)
            q = "SELECT document_file_size FROM tbl_bulk_past_data " + \
                "where csv_past_id= %s and compliance_task_name=%s " + \
                " and perimary_legislation = %s and " + \
                " secondary_legislation = %s and " \
                "compliance_description = %s and due_date= %s and " + \
                "unit_code = %s"
            params = [
                csv_id, d["compliance_task_name"],
                d["perimary_legislation"], d["secondary_legislation"],
                d["compliance_description"], d["due_date"],
                d["unit_code"]
            ]
            rows = db.select_all(q, params)
            if rows:
                document_size = rows[0]["document_file_size"]
                columns.append("document_size")
                values.append(document_size)
            if values:
                self._source_db.insert(
                    "tbl_compliance_history", columns, values)
                self._source_db.commit()
        return True

    # main db related validation mapped with field name
    def status_check_methods(self):
        self._validation_method_maps = {
            "Legal_Entity": self.check_legal_entity,
            "Domain": self.check_domain,
            "Unit_Code": self.check_unit_code,
            "Unit_Name": self.check_unit_name,
            "Primary_Legislation": self.check_primary_legislation,
            "Secondary_Legislation": self.check_secondary_legislation,
            "Compliance_Task": self.check_compliance_task,
            "Compliance_Description": self.check_compliance_description,
            "Compliance_Frequency": self.check_frequency,
            "Assignee": self.check_assignee,
            "Due_Date": self.check_due_date,
            "Completion_Date": self.check_completion_date
        }

    def csv_column_fields(self):
        self._csv_column_name = [
            "Legal_Entity", "Domain",
            "Unit_Code", "Unit_Name",
            "Primary_Legislation", "Secondary_Legislation",
            "Compliance_Task", "Compliance_Description",
            "Compliance_Frequency", "Statutory_Date",
            "Due_Date", "Assignee", "Completion_Date",
            "Document_Name"
        ]


class ValidateCompletedTaskCurrentYearCsvData(SourceDB):
    def __init__(self, db, source_data, session_user, csv_name, csv_header):
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._legal_entity_names = None
        self._domains = None
        self._error_summary = {}
        self.error_summary()

        self._sheet_name = "Completed_Task_Current_Year-Pas"

    # error summary mapped with initial count
    def error_summary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error": 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0,
            "invalid_date": 0,
            "invalid_file_format": 0
        }

    def compare_csv_columns(self):
        res = collections.Counter(
            self._csv_column_name) == collections.Counter(self._csv_header)
        return res
    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''

    def make_error_desc(self, res, msg):
            if res is True:
                res = []
            if res is not True:
                if type(msg) is list:
                    res.extend(msg)
                else:
                    res.append(msg)
            return res

    def validate_csv_values(
        self, res, values, key, csv_param, data,
        mapped_error_dict, mapped_header_dict, invalid,
        is_found, error_count
    ):
        for v in [v.strip() for v in values]:
            valid_failed, error_cnt = parse_csv_dictionary_values(
                key, v)
            if valid_failed is not True:
                if res is True:
                    res = valid_failed
                    error_count = error_cnt
                else:
                    res.extend(valid_failed)
                    error_count["mandatory"] += error_cnt["mandatory"]
                    error_count["max_length"] += error_cnt[
                        "max_length"]
                    error_count["invalid_char"] += error_cnt[
                        "invalid_char"]
                    error_count["invalid_date"] += error_cnt[
                        "invalid_date"]
            if v != "":
                if csv_param.get(
                    "check_is_exists"
                ) is True or csv_param.get(
                    "check_is_active"
                ) is True or csv_param.get(
                    "check_due_date"
                ) is True or csv_param.get(
                    "check_completion_date"
                ) is True:
                    unbound_method = self._validation_method_maps.get(
                        key)
                    if unbound_method is not None:
                        if key == "Due_Date":
                            is_found = unbound_method(
                                v, data.get("Domain"),
                                data.get("Unit_Code"),
                                data.get("Compliance_Task"),
                                data.get("Primary_Legislation"),
                                data.get("Secondary_Legislation"),
                                data.get("Compliance_Description"),
                            )
                        elif key == "Completion_Date":
                            is_found = unbound_method(
                                data.get("Unit_Code"),
                                data.get("Due_Date"),
                                data.get("Compliance_Task"),
                                data.get("Domain"),
                                data.get("Completion_Date")
                            )
                        elif key == "Compliance_Frequency":
                            is_found = unbound_method(
                                data.get("Compliance_Task"),
                                data.get("Compliance_Frequency")
                            )
                        elif key == "Unit_Code":
                            is_found = unbound_method(
                                v, data.get("Unit_Name")
                            )
                        elif key == "Primary_Legislation":
                            is_found = unbound_method(
                                v, data.get("Unit_Code")
                            )
                        elif key == "Secondary_Legislation":
                            is_found = unbound_method(
                                v, data.get("Primary_Legislation")
                            )
                        elif key == "Compliance_Task":
                            is_found = unbound_method(
                                v, data.get("Primary_Legislation"),
                                data.get("Secondary_Legislation")
                            )
                        elif key == "Compliance_Description":
                            is_found = unbound_method(
                                v, data.get("Primary_Legislation"),
                                data.get("Secondary_Legislation"),
                                data.get("Compliance_Task")
                            )
                        else:
                            is_found = unbound_method(v)
                    if is_found is False:
                        return is_found
                    elif is_found is None:
                        pass
                    elif is_found is not True and is_found != "":
                        msg = "%s - %s" % (key, is_found)
                        if res is not True:
                            res.append(msg)
                        else:
                            res = [msg]
                        if "Status" in str(is_found):
                            self._error_summary["inactive_error"] += 1
                        else:
                            self._error_summary[
                                "invalid_data_error"] += 1
        return (
            mapped_error_dict, mapped_header_dict, invalid, error_count,
            res
        )

    def validate_csv_data(
        self, row_idx, res, data, _csv_column_name,
        mapped_error_dict, mapped_header_dict, invalid,
        error_count
    ):
        for key in _csv_column_name:
            value = data.get(key)
            is_found = ""
            if key == "Compliance_Frequency":
                value = "".join(e for e in value if e.isalnum())
            values = value.strip().split(CSV_DELIMITER)
            csv_param = csv_params.get(key)
            result = self.validate_csv_values(
                res, values, key, csv_param, data,
                mapped_error_dict, mapped_header_dict, invalid,
                is_found, error_count
            )
            if result is not False:
                (
                    mapped_error_dict, mapped_header_dict,
                    invalid, error_count, res
                ) = result
            else:
                return False
            if key is "Document_Name":
                msg = []
                doc_name = data["Document_Name"]
                if doc_name != "":
                    file_extension = os.path.splitext(
                        data["Document_Name"])
                    allowed_file_formats = [
                        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
                        ".png", ".jpeg"
                    ]
                    if file_extension[1] not in allowed_file_formats:
                        msg.append("Document Name - Invalid File Format")
                        self._error_summary["invalid_file_format"] += 1
                        res = self.make_error_desc(res, msg)
                    if doc_name in self._doc_names:
                        msg.append("Document Name - Duplicate document name")
                        res = self.make_error_desc(res, msg)
                    else:
                        self._doc_names.append(doc_name)
            if res is not True:
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else:
                    error_list.extend(res)
                res = True

                mapped_error_dict[row_idx] = error_list
                head_idx = mapped_header_dict.get(key)
                if head_idx is None:
                    head_idx = [row_idx]
                else:
                    head_idx.append(row_idx)

                mapped_header_dict[key] = head_idx
                invalid += 1
                self._error_summary["mandatory_error"] += error_count[
                    "mandatory"]
                self._error_summary["max_length_error"] += error_count[
                    "max_length"]
                self._error_summary["invalid_char_error"] += error_count[
                    "invalid_char"]
                self._error_summary["invalid_date"] += error_count[
                    "invalid_date"]
        return (
            mapped_error_dict, mapped_header_dict, invalid, error_count
        )

    def check_if_already_saved_compliance(self, legal_entity_id):
        for row_idx, data in enumerate(self._source_data):
            compliance_task_name = data.get("Compliance_Task")
            primary_legislation = data.get("Primary_Legislation")
            secondary_legislation = data.get("Secondary_Legislation")
            unit_code = data.get("Unit_Code")
            due_date = data.get("Due_Date")
            compliance_name = self.get_compliance_task_name(
                compliance_task_name)
            description = data.get("Compliance_Description")
            frequency = data.get("Compliance_Frequency")
            q = "SELECT compliance_history_id " + \
                " from tbl_compliance_history " + \
                " where compliance_id = (" + \
                " SELECT compliance_id FROM tbl_compliances where " + \
                "compliance_task = TRIM(%s) and compliance_description = " + \
                " TRIM(%s) and (statutory_mapping like %s || " + \
                " statutory_mapping like %s) and " + \
                " frequency_id = (SELECT frequency_id from " + \
                " tbl_compliance_frequency WHERE " + \
                " frequency=TRIM(%s)) Limit 1) and unit_id =( select " + \
                " unit_id from tbl_units where unit_code = %s and " + \
                " legal_entity_id = %s ) " + \
                " and date(due_date) = %s"
            try:
                due_date = datetime.strptime(due_date, "%d-%b-%Y").date()
            except ValueError:
                pass
            legis_cond = '%"' + primary_legislation
            legis_cond1 = legis_cond
            if secondary_legislation != "":
                legis_cond += ">>" + secondary_legislation + "%"
                legis_cond1 += " >> " + secondary_legislation + "%"
            else:
                legis_cond += "%"
                legis_cond1 += "%"
            params = [
                compliance_name, description, legis_cond, legis_cond1,
                frequency, unit_code, legal_entity_id, due_date
            ]
            self.connect_source_db(legal_entity_id)
            rows = self._source_db.select_all(q, params)
            if len(rows) > 0:
                return False

    def perform_validation(self, legal_entity_id):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        res = True
        if not self.compare_csv_columns():
            res = False
            return res
        self.init_values(legal_entity_id)
        error_count = {
            "mandatory": 0, "max_length": 0, "invalid_char": 0,
            "invalid_date": 0
        }
        for row_idx, data in enumerate(self._source_data):
            if row_idx == 0:
                self._legal_entity_names = data.get("Legal_Entity")
                self._domains = data.get("Domain")
            result = self.validate_csv_data(
                row_idx, res, data, self._csv_column_name,
                mapped_error_dict, mapped_header_dict, invalid,
                error_count
            )
            if result is False:
                return result
            else:
                (
                    mapped_error_dict, mapped_header_dict, invalid,
                    error_count
                ) = result
        if invalid > 0:
            return self.make_invalid_return(
                mapped_error_dict, mapped_header_dict)
        else:
            return self.make_valid_return(
                mapped_error_dict, legal_entity_id)

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        file_string = self._csv_name.split(".")
        file_name = "%s_%s.%s" % (
            file_string[0], "invalid", "xlsx"
        )
        final_hearder = self._csv_header
        final_hearder.append("Error Description")
        write_data_to_excel(
            os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"),
            file_name, final_hearder,
            self._source_data, mapped_error_dict, mapped_header_dict,
            self._sheet_name
        )
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        # make csv file
        rename_file_type(file_name, "csv")
        # make ods file
        rename_file_type(file_name, "ods")
        # make text file
        rename_file_type(file_name, "txt")
        return {
            "return_status": False,
            "invalid_file": file_name,
            "mandatory_error": self._error_summary["mandatory_error"],
            "max_length_error": self._error_summary["max_length_error"],
            "duplicate_error": self._error_summary["duplicate_error"],
            "invalid_char_error": self._error_summary["invalid_char_error"],
            "invalid_data_error": self._error_summary["invalid_data_error"],
            "inactive_error": self._error_summary["inactive_error"],
            "total": total,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "invalid_file_format": self._error_summary["invalid_file_format"],
            "invalid_date": self._error_summary["invalid_date"]
        }

    def make_valid_return(
        self, mapped_error_dict, legal_entity_id
    ):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        if total <= 0:
            return False
        unit_code = self._source_data[0]["Unit_Code"]
        domain_name = self._source_data[0]["Domain"]

        self.connect_source_db(legal_entity_id)

        unit_code = [unit_code]
        q = "select unit_id from tbl_units where unit_code = TRIM(%s)"
        unit_id = self._source_db.select_all(q, unit_code)
        unit_id = unit_id[0]["unit_id"]

        domain_name = [domain_name]
        q = "select domain_id from tbl_domains where domain_name = TRIM(%s)"
        domain_id = self._source_db.select_all(q, domain_name)
        domain_id = domain_id[0]["domain_id"]

        return {
            "return_status": True,
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "doc_names": list(set(self._doc_names)),
            "unit_id": unit_id,
            "domain_id": domain_id,
        }


class ValidateCompletedTaskForSubmit(SourceDB):
    def __init__(self, db, csv_id, data_result, session_user):
        SourceDB.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._session_user_obj = session_user
        self._source_data = data_result
        self.doc_count = 0
        self.get_file_count(db)

    def get_file_count(self, db):
        query = "select total_documents from tbl_bulk_past_data_csv " + \
                "where csv_past_id = %s"
        param = [self._csv_id]
        doc_rows = db.select_all(query, param)
        doc_count = 0
        for d in doc_rows:
            doc_count = d.get("total_documents")

        self.doc_count = doc_count

    def check_for_duplicate_records(self, legal_entity_id):
        for row_idx, data in enumerate(self._source_data):
            compliance_task_name = data.get("compliance_task_name")
            primary_legislation = data.get("perimary_legislation")
            secondary_legislation = data.get("secondary_legislation")
            unit_code = data.get("unit_code")
            due_date = data.get("due_date")
            compliance_name = self.get_compliance_task_name(
                compliance_task_name)
            description = data.get("compliance_description")
            frequency = data.get("compliance_frequency")
            q = "SELECT compliance_history_id " + \
                " from tbl_compliance_history " + \
                " where compliance_id = (" + \
                " SELECT compliance_id FROM tbl_compliances where " + \
                "compliance_task = TRIM(%s) and compliance_description = " + \
                " TRIM(%s) and statutory_mapping like %s and " + \
                " frequency_id = (SELECT frequency_id from " + \
                " tbl_compliance_frequency WHERE " + \
                " frequency=TRIM(%s)) Limit 1) and unit_id =( select " + \
                " unit_id from tbl_units where unit_code = %s and " + \
                " legal_entity_id = %s ) " + \
                " and date(due_date) = %s"
            # try:
            #     due_date = datetime.strptime(due_date, "%d-%b-%Y")
            # except ValueError:
            #     pass
            legis_cond = '["' + primary_legislation
            if secondary_legislation != "":
                legis_cond += ">>" + secondary_legislation + "%"
            else:
                legis_cond += "%"
            params = [
                compliance_name, description, legis_cond,
                frequency, unit_code, legal_entity_id, due_date.date()
            ]
            self.connect_source_db(legal_entity_id)
            rows = self._source_db.select_all(q, params)
            if len(rows) > 0:
                return False

    def document_download_process_initiate(
        self, csvid, country_id, legal_id, domain_id, unit_id, session_token
    ):
        self.file_server_approve_call(
            csvid, country_id, legal_id, domain_id, unit_id
        )
        self._stop = False

        def check_status():
            if self._stop:
                return

            file_status = get_file_stats(csvid)
            if file_status == "completed":
                self._stop = True
                self.call_file_server(
                    csvid, country_id, legal_id, domain_id, unit_id,
                    session_token
                )

            if self._stop is False:
                t = threading.Timer(60, check_status)
                t.daemon = True
                t.start()

        def get_file_stats(csvid):
            file_status = None
            c_db_con = bulkupload_db_connect()
            _db_check = Database(c_db_con)
            try:
                _db_check.begin()
                query = "select file_download_status from " \
                        "tbl_bulk_past_data_csv where csv_past_id = %s"
                param = [csvid]

                data = _db_check.select_all(query, param)
                if len(data) > 0:
                    file_status = data[0].get("file_download_status")
            except Exception:
                _db_check.rollback()

            finally:
                _db_check.close()
                c_db_con.close()
            return file_status

        check_status()

    def file_server_approve_call(
        self, csvid, country_id, legal_id, domain_id, unit_id
    ):
        caller_name = (
            "%sdocsubmit?csvid=%s&c_id=%s&le_id=%s&d_id=%s&u_id=%s"
        ) % (
            CLIENT_TEMP_FILE_SERVER, csvid, country_id, legal_id,
            domain_id, unit_id
        )
        response = requests.post(caller_name)
        return response

    def call_file_server(
        self, csvid, country_id, legal_id, domain_id, unit_id, session_token
    ):
        file_server_ip = None
        file_server_port = None
        query = "select ip, port from tbl_file_server where " + \
            "file_server_id = (select file_server_id from " + \
            " tbl_client_database where legal_entity_id = %s )"
        param = [legal_id]
        self.connect_source_db(legal_id)
        docRows = self._knowledge_db.select_all(query, param)
        if docRows > 0:
            file_server_ip = docRows[0]["ip"]
            file_server_port = docRows[0]["port"]
        else:
            return "File server not available"

        current_date = datetime.now().strftime("%d-%b-%Y")
        client_id = str(session_token).split("-")[0]
        caller = (
            "http://%s:%s/clientfile?csvid=%s&c_id=%s&le_id=%s"
            "&d_id=%s&u_id=%s&start_date=%s&client_id=%s") % (
            file_server_ip, file_server_port, csvid, country_id, legal_id,
            domain_id, unit_id, current_date, client_id
        )
        try:
            response = requests.post(caller)
        except ConnectionError as e:
            print e
            response = "error"
        self.save_file_submit_status(response)
        print "RESPONSE ->> ", response
        return response

    def frame_data_for_main_db_insert(
        self, db, data_result, legal_entity_id, csv_id
    ):
        data_save_status = self.save_completed_task_data(
            db, data_result, legal_entity_id, csv_id
        )
        self.save_data_submit_status(data_save_status)
        return data_save_status

    def save_data_submit_status(self, data_save_status):
        data_submit_value = 0
        if data_save_status is True:
            data_submit_value = 1
        else:
            data_submit_value = 2

        query = "UPDATE tbl_bulk_past_data_csv SET " + \
                "data_submit_status = %s WHERE csv_past_id = %s"

        self._db.execute(query, [data_submit_value, self._csv_id])

    def save_file_submit_status(self, response):
        file_submit_value = 0
        if str(response).find("200") >= 0:
            file_submit_value = 1
        else:
            file_submit_value = 2

        file_down_status = "completed"
        if file_submit_value == 2:
            file_down_status = None

        bulk_db_con = bulkupload_db_connect()
        bulk_db_check = Database(bulk_db_con)
        try:
            bulk_db_check.begin()
            query = "UPDATE tbl_bulk_past_data_csv SET " + \
                " file_submit_status = %s AND file_download_status = %s" + \
                " WHERE csv_past_id = %s"
            param = [file_submit_value, file_down_status, self._csv_id]

            bulk_db_check.execute(query, param)
            bulk_db_check.commit()
        except Exception, e:
            print e
            bulk_db_check.rollback()

        finally:
            bulk_db_check.close()
            bulk_db_con.close()


def bulkupload_db_connect():
    cnx_pool = mysql.connector.connect(
        user=BULK_UPLOAD_DB_USERNAME,
        password=BULK_UPLOAD_DB_PASSWORD,
        host=BULK_UPLOAD_DB_HOST,
        database=BULK_UPLOAD_DATABASE_NAME,
        port=BULK_UPLOAD_DB_PORT,
        autocommit=False,
    )
    return cnx_pool
