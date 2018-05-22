import os
from datetime import datetime, timedelta
import collections
import mysql.connector
import requests
import threading
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from bulkupload.client_bulkconstants import (
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH, TEMP_FILE_SERVER, FILE_SERVER,
    BULK_UPLOAD_DB_USERNAME, BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DB_HOST,
    BULK_UPLOAD_DATABASE_NAME, BULK_UPLOAD_DB_PORT
)
from ..buapiprotocol.pastdatadownloadbulk import (
        calculate_final_due_dates, return_past_due_dates
    )
from client_keyvalidationsettings import (
        csv_params, parse_csv_dictionary_values
    )
from ..client_bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)

# from  clientprotocol.clienttransactions import ()
from server.common import get_date_time

# from server.clientdatabase.general import ( is_two_levels_of_approval )

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
        self.Legal_Entity = {}
        self.Domain = {}
        self.Unit_Code = {}
        self.Unit_Name = {}
        self.Statutories = {}
        self.Compliance_Task = {}
        self.Compliance_Description = {}
        self.Compliance_Frequency = {}
        self.Assignee = {}
        # self.connect_source_db()
        self._validation_method_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()
        self._doc_names = []
        # self.get_doc_names()

    def connect_source_db(self, legal_entity_id):
        self._knowledge_db_con = mysql.connector.connect(
                user=KNOWLEDGE_DB_USERNAME,
                password=KNOWLEDGE_DB_PASSWORD,
                host=KNOWLEDGE_DB_HOST,
                database=KNOWLEDGE_DATABASE_NAME,
                port=KNOWLEDGE_DB_PORT,
                autocommit=False)

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

        # self._source_db_con = mysql.connector.connect(
        #     user=KNOWLEDGE_DB_USERNAME,
        #     password=KNOWLEDGE_DB_PASSWORD,
        #     host=KNOWLEDGE_DB_HOST,
        #     database="compfie_le_att_1",
        #     port=KNOWLEDGE_DB_PORT,
        #     autocommit=False,
        # )
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

    def get_legal_entities(self):
        query = "SELECT legal_entity_id, legal_entity_name, " + \
            "is_closed FROM tbl_legal_entities;"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_domains(self):
        query = "SELECT domain_id, domain_name, is_active  FROM tbl_domains"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Domain[d["domain_name"]] = d

    def get_unit_code(self):
        query = "SELECT unit_id, client_id, legal_entity_id, " + \
            "unit_code, unit_name, is_closed FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Unit_Code[d["unit_code"]] = d

    def get_unit_name(self):
        query = "SELECT unit_id, client_id, legal_entity_id, " + \
            "unit_code, unit_name, is_closed FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Unit_Name[d["unit_name"]] = d

    def get_primary_legislation(self):
        query = "select trim(SUBSTRING_INDEX" + \
            " (SUBSTRING_INDEX((TRIM(TRAILING '\"]' " + \
            "FROM TRIM(LEADING '[\"' FROM t.statutory_mapping)))," + \
            " '>>',1),'>>',- 1)) AS primary_legislation, " + \
            " trim(SUBSTRING_INDEX(SUBSTRING_INDEX( " + \
            " CONCAT(TRIM(TRAILING '\"]' " + \
            " FROM TRIM(LEADING '[\"' " + \
            " FROM t.statutory_mapping)),'>>'),'>>',2),'>>',- 1)) " + \
            " AS secondary_legislation from tbl_compliances t"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Statutories[d["primary_legislation"]] = d

    def get_secondary_legislation(self):
        query = "select trim(SUBSTRING_INDEX(" + \
            " SUBSTRING_INDEX((TRIM(TRAILING '\"]' " + \
            "FROM TRIM(LEADING '[\"' " + \
            " FROM t.statutory_mapping))),'>>',1),'>>',- 1)) " + \
            " AS primary_legislation, trim(SUBSTRING_INDEX( " + \
            " SUBSTRING_INDEX(CONCAT(TRIM(TRAILING '\"]' " + \
            " FROM TRIM(LEADING '[\"' FROM t.statutory_mapping) " + \
            "),'>>'),'>>',2),'>>',- 1)) AS secondary_legislation " + \
            " from tbl_compliances t;"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Statutories[d["secondary_legislation"]] = d

    def get_compliance_task(self):
        query = "SELECT compliance_id, statutory_provision, " + \
            "case when ifnull(document_name,'') = '' then " + \
            "trim(compliance_task) else trim(Concat_ws( " + \
            "' - ',document_name, compliance_task)) end AS " + \
            " compliance_task, compliance_description, " + \
            "is_active from tbl_compliances"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Task[d["compliance_task"]] = d

    def get_compliance_description(self):
        query = "SELECT compliance_id, statutory_provision, " + \
            " compliance_task, compliance_description, is_active " + \
            "from tbl_compliances"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Description[d["compliance_description"]] = d

    def get_compliance_frequency(self):
        query = "select frequency_id, frequency " + \
            " from tbl_compliance_frequency " + \
                " where frequency_id in (2,3)"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Frequency[d["frequency"]] = d

    def get_assignee(self):
        query = "SELECT Distinct assignee as ID, employee_code," + \
                " employee_name, " + \
                " CONCAT_WS(' - ', employee_code, employee_name) " + \
                " As Assignee " + \
                " FROM tbl_assign_compliances ac INNER JOIN " + \
                " tbl_users u ON (ac.assignee = u.user_id)"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Assignee[d["Assignee"]] = d

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

    def return_unit_domain_id(self, domain_name, unit_name):
        query = "SELECT domain_id from tbl_domains " + \
                "where domain_name  = '%s'" % domain_name
        rows = self._source_db.select_all(query)
        domain_id = rows[0]["domain_id"]
        query = "SELECT unit_id from tbl_units " + \
                "where unit_name  = '%s'" % unit_name
        rows = self._source_db.select_all(query)
        unit_id = rows[0]["unit_id"]
        return unit_id, domain_id

    def check_due_date(
        self, due_date, domain_name, unit_name, level_1_statutory_name
    ):
        (unit_id, domain_id) = self.return_unit_domain_id(
            domain_name, unit_name)
        rows = return_past_due_dates(
                self._source_db, domain_id, unit_id,
                level_1_statutory_name
            )
        print "rows: %s" % rows
        due_dates = calculate_final_due_dates(
                self._source_db, rows, domain_id, unit_id
            )
        try:
            due_date = datetime.datetime.strptime(due_date, "%d-%b-%Y")
            due_date = due_date.date().strftime("%Y-%m-%d")
        except:
            return "Not Found"
        if due_date in due_dates[0]:
            return True
        else:
            return "Not Found"

    def check_completion_date(
        self, completion_date, statutory_date, due_date
    ):
        statu_array = statutory_date.split()
        trigger_before_days_string = statu_array[len(statu_array)-1]
        trigger_before_days = int(
            trigger_before_days_string.strip(")(")
        )
        try:
            due_date = datetime.datetime.strptime(
                due_date, "%d-%b-%Y")
        except:
            return True
        start_date = due_date.date() - timedelta(days=trigger_before_days)
        try:
            completion_date = datetime.datetime.strptime(
                completion_date, "%d-%b-%Y")
        except:
            return "Invalid Date"
        if completion_date.date() < start_date:
            return "Should be greater than Start Date"
        else:
            return True

    # def check_client_group(self, group_name):
    #     return self.check_base(True, self.Client_Group, group_name, None)

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(
            True, self.Legal_Entity, legal_entity_name, None
        )

    def check_domain(self, domain_name):
        return self.check_base(True, self.Domain, domain_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(True, self.Unit_Code, unit_code, None)

    def check_unit_name(self, unit_name):
        return self.check_base(True, self.Unit_Name, unit_name, None)

    def check_primary_legislation(self, statutories):
        return self.check_base(False, self.Statutories, statutories, None)

    def check_secondary_legislation(self, statutories):
        return self.check_base(False, self.Statutories, statutories, None)

    def check_compliance_task(self, compliance_task):
        return self.check_base(
            True, self.Compliance_Task, compliance_task, None)

    def check_compliance_description(self, compliance_description):
        return self.check_base(
            True, self.Compliance_Description, compliance_description, None)

    def check_frequency(
            self, frequency):
        return self.check_base(
            False, self.Compliance_Frequency, frequency, None)

    def check_assignee(self, assignee):
        return self.check_base(False, self.Assignee, assignee, None)

    def is_two_levels_of_approval(_source_db):
        query = "SELECT two_levels_of_approval FROM tbl_reminder_settings"
        rows = _source_db.select_all(query)
        return bool(rows[0]["two_levels_of_approval"])

    def save_completed_task_data(self, data, legal_entity_id, session_user):
        # self.connect_source_db(legal_entity_id)
        is_two_level = False
        compliance_id = ""
        unit_id = ""

        # created_on = get_date_time()

        # "documents",
        columns = []
        # columns = [
        #     "legal_entity_id", "unit_id", "compliance_id", "start_date",
        #     "due_date", "completion_date", "completed_by",
        #     "completed_on",
        #     "approve_status", "approved_by", "approved_on", "current_status"
        # ]

        values = []
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
            cName = [
                d["compliance_task_name"], d["compliance_description"],
                d["compliance_frequency"]
            ]
            q = "SELECT compliance_id FROM tbl_compliances where " + \
                "compliance_task = TRIM(%s) and compliance_description = " + \
                "TRIM(%s) and frequency_id = (SELECT frequency_id from " + \
                " tbl_compliance_frequency WHERE frequency=TRIM(%s))"

            compliance_id = self._source_db.select_all(q, cName)
            compliance_id = compliance_id[0]["compliance_id"]

            completion_date = d["completion_date"]

            # Unit ID
            unitCode = [d["unit_code"]]
            print "unitCode >>>> ", unitCode
            q = "select unit_id from tbl_units where unit_code = TRIM(%s)"
            unit_id = self._source_db.select_all(q, unitCode)
            print "unit_id ->> ", unit_id
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
            tblAssignCompliances = "tbl_assign_compliances"
            rows = self._source_db.get_data(
                tblAssignCompliances,
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
            if values:
                self._source_db.insert(
                    "tbl_compliance_history", columns, values)
                self._source_db.commit()
        return True

    # main db related validation mapped with field name
    def statusCheckMethods(self):
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
        self._Domains = None
        # self._Unit_Codes = None
        # self._Unit_Names = None
        self._error_summary = {}
        self.errorSummary()

        self._sheet_name = "Completed_Task_Current_Year-Pas"

    # error summary mapped with initial count
    def errorSummary(self):
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
        res = collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)
        return res
    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''

    def perform_validation(self, legal_entity_id):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        res = True
        if not self.compare_csv_columns():
            res = False
            return res
        self.init_values(legal_entity_id)

        def make_error_desc(res, msg):
            if res is True:
                res = []
            if res is not True:
                if type(msg) is list:
                    res.extend(msg)
                else:
                    res.append(msg)
            return res
        for row_idx, data in enumerate(self._source_data):
            if row_idx == 0:
                self._legal_entity_names = data.get("Legal_Entity")
                self._Domains = data.get("Domain")

            res = True
            error_count = {
                "mandatory": 0, "max_length": 0, "invalid_char": 0,
                "invalid_date": 0
                }
            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)
                if (key == "Document_Name" and value != ''):
                    self._doc_names.append(value)
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
                        if csvParam.get(
                                "check_is_exists"
                                ) is True or csvParam.get(
                                "check_is_active"
                                ) is True or csvParam.get(
                                "check_due_date"
                                ) is True or csvParam.get(
                                "check_completion_date"
                                ) is True:
                            unboundMethod = self._validation_method_maps.get(
                                key)

                            if unboundMethod is not None:
                                if key == "Due_Date":
                                    isFound = unboundMethod(
                                        v, data.get("Domain"),
                                        data.get("Unit_Name"),
                                        data.get("Primary_Legislation")
                                    )
                                elif key == "Completion_Date":
                                    isFound = unboundMethod(
                                        v, data.get("Statutory_Date"),
                                        data.get("Due_Date")
                                    )
                                else:
                                    isFound = unboundMethod(v)
                            if isFound is not True and isFound != "":
                                msg = "%s - %s" % (key, isFound)
                                print "msg: %s" % msg
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]
                                if "Status" in str(isFound):
                                    self._error_summary["inactive_error"] += 1
                                else:
                                    self._error_summary[
                                        "invalid_data_error"] += 1
                if key is "Document_Name":
                    msg = []
                    if data["Document_Name"] != "":
                        file_extension = os.path.splitext(
                            data["Document_Name"])
                        allowed_file_formats = [".pdf", ".doc", ".docx",
                                                ".xls", ".xlsx"]
                        if file_extension[1] not in allowed_file_formats:
                            msg.append("Document Name - Invalid File Format")
                            self._error_summary["invalid_file_format"] += 1
                            res = make_error_desc(res, msg)
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

        if invalid > 0:
            return self.make_invalid_return(
                mapped_error_dict, mapped_header_dict)
        else:
            return self.make_valid_return(
                mapped_error_dict, mapped_header_dict, legal_entity_id)

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        fileString = self._csv_name.split('.')
        file_name = "%s_%s.%s" % (
            fileString[0], "invalid", "xlsx"
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
            "duplicate_error" : self._error_summary["duplicate_error"],
            "invalid_char_error": self._error_summary["invalid_char_error"],
            "invalid_data_error": self._error_summary["invalid_data_error"],
            "inactive_error": self._error_summary["inactive_error"],
            "total": total,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "invalid_file_format": self._error_summary["invalid_file_format"],
            "invalid_date": self._error_summary["invalid_date"]
        }


    def make_valid_return(self, mapped_error_dict, mapped_header_dict, legal_entity_id):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        Unit_Code = self._source_data[0]["Unit_Code"]
        domain_name = self._source_data[0]["Domain"]

        self.connect_source_db(legal_entity_id)

        unitCode = [Unit_Code]
        q = "select unit_id from tbl_units where unit_code = TRIM(%s)"
        unit_id = self._source_db.select_all(q, unitCode)
        unit_id = unit_id[0]["unit_id"]

        domainName = [domain_name]
        q = "select domain_id from tbl_domains where domain_name = TRIM(%s)"
        domain_id = self._source_db.select_all(q, domainName)
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
    def __init__(self, db, csv_id, dataResult, session_user):
        SourceDB.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._session_user_obj = session_user
        self._source_data = dataResult
        self._doc_count = 0
        # self.get_source_data()
        self.get_file_count(db)

        # self._declined_row_idx = []
        # self._legal_entity = None
        # self._client_group = None
        # self._csv_name = None
        # self._unit_id = None

    def get_file_count(self, db):
        query = "select total_documents from tbl_bulk_past_data_csv " + \
                "where csv_past_id = %s"
        param = [self._csv_id]
        docRows = db.select_all(query, param)

        for d in docRows:
            doc_count = d.get("total_documents")

        self._doc_count = doc_count

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
                # data = _db_check.call_proc(
                #     "sp_pastdata_get_file_download_status", [csvid]
                # )
                query = "select file_download_status from " \
                        "tbl_bulk_past_data_csv where csv_past_id = %s"
                param = [csvid]

                data = _db_check.select_all(query, param)
                print "DAta -> ", data
                if len(data) > 0:
                    file_status = data[0].get("file_download_status")

            except Exception, e:
                print e
                _db_check.rollback()

            finally:
                _db_check.close()
                c_db_con.close()
            return file_status

        check_status()


    def file_server_approve_call(
        self, csvid, country_id, legal_id, domain_id, unit_id
    ):
        print "Approve call done"
        caller_name = "%sdocsubmit?csvid=%s&c_id=%s&le_id=%s&d_id=%s&u_id=%s" % (
            TEMP_FILE_SERVER, csvid, country_id, legal_id, domain_id, unit_id)
        print "caller_name", caller_name
        response = requests.post(caller_name)

    def call_file_server(
        self, csvid, country_id, legal_id, domain_id, unit_id, session_token
    ):
        print "Call to File Server"
        current_date = datetime.datetime.now().strftime('%d-%b-%Y')
        print "client id----> ", str(session_token).split('-')[0]
        client_id = str(session_token).split('-')[0]
        caller = "%sclientfile?csvid=%s&c_id=%s&le_id=%s&d_id=%s&u_id=%s&start_date=%s&client_id=%s" % (
            FILE_SERVER, csvid, country_id, legal_id, domain_id, unit_id, current_date, client_id)
        print "caller-> ", caller
        response = requests.post(caller)
        print "response>> ", response

    def frame_data_for_main_db_insert(
        self, db, dataResult, legal_entity_id, session_user
    ):
        # self.get_source_data()
        # self._source_data.sort(key=lambda x: (
        #      x["Domain"], x["Unit_Name"]
        # ))
        # for k, v in groupby(self._source_data, key=lambda s: (
        #     s["Domain"], s["Unit_Name"]
        # )):
        #     grouped_list = list(v)
        #     if len(grouped_list) == 0:
        #         continue

        #     unit_id = None
        #     domain_id = None
        #     value = grouped_list[0]

        #     unit_id = self.Unit_Code.get(value.get("Unit_Code")).get("unit_id")
        #     domain_id = self.Domain.get(value.get("Domain")).get("domain_id")

            # cs_id = self.save_client_statutories_data(
            #     self._client_id, unit_id, domain_id, user_id
            #     )
        return self.save_completed_task_data(
            dataResult, legal_entity_id, session_user
        )


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
