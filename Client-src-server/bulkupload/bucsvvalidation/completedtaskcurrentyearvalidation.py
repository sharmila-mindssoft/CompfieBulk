import os
import collections
import mysql.connector
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)
from bulkupload.client_bulkconstants import(
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH
)

from client_keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..client_bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)
from server.common import ( get_date_time )

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

    def connect_source_db(self, legal_entity_id):
        # print "completedtaskcurrentyearvalidation>self.legal_entity_id>>", legal_entity_id

        self._knowledge_db_con = mysql.connector.connect(
        user=KNOWLEDGE_DB_USERNAME,
        password=KNOWLEDGE_DB_PASSWORD,
        host=KNOWLEDGE_DB_HOST,
        database=KNOWLEDGE_DATABASE_NAME,
        port=KNOWLEDGE_DB_PORT,
        autocommit=False, )

        self._knowledge_db = Database(self._knowledge_db_con)
        self._knowledge_db.begin()

        query = "select t1.client_database_id, t1.database_name, t1.database_username, t1.database_password, t3.database_ip, database_port from tbl_client_database_info as t1 inner join tbl_client_database as t2 on t2.client_database_id = t1.client_database_id inner join tbl_database_server as t3 on t3.database_server_id = t2.database_server_id where t1.db_owner_id = %s and t1.is_group = 0;"
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
        # print "init_values(self)>>>>"
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
        query = "SELECT legal_entity_id, legal_entity_name, is_closed FROM tbl_legal_entities;"
        rows = self._source_db.select_all(query)
        for d in rows :
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_domains(self):
        query = "SELECT domain_id, domain_name, is_active  FROM tbl_domains"
        rows = self._source_db.select_all(query)
        for d in rows :
            self.Domain[d["domain_name"]] = d

    def get_unit_code(self):
        query = "SELECT unit_id, client_id, legal_entity_id, unit_code, unit_name, is_closed FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Unit_Code[d["unit_code"]] = d

    def get_unit_name(self):
        query = "SELECT unit_id, client_id, legal_entity_id, unit_code, unit_name, is_closed FROM tbl_units"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Unit_Name[d["unit_name"]] = d

    def get_primary_legislation(self):
        query = "select trim(SUBSTRING_INDEX(SUBSTRING_INDEX((TRIM(TRAILING '\"]' FROM TRIM(LEADING '[\"' FROM t.statutory_mapping))),'>>',1),'>>',- 1)) AS primary_legislation, trim(SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(TRIM(TRAILING '\"]' FROM TRIM(LEADING '[\"' FROM t.statutory_mapping)),'>>'),'>>',2),'>>',- 1)) AS secondary_legislation from tbl_compliances t"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Statutories[d["primary_legislation"]] = d

    def get_secondary_legislation(self):
        query = "select trim(SUBSTRING_INDEX(SUBSTRING_INDEX((TRIM(TRAILING '\"]' FROM TRIM(LEADING '[\"' FROM t.statutory_mapping))),'>>',1),'>>',- 1)) AS primary_legislation, trim(SUBSTRING_INDEX(SUBSTRING_INDEX(CONCAT(TRIM(TRAILING '\"]' FROM TRIM(LEADING '[\"' FROM t.statutory_mapping)),'>>'),'>>',2),'>>',- 1)) AS secondary_legislation from tbl_compliances t;"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Statutories[d["secondary_legislation"]] = d

    def get_compliance_task(self):
        query = "SELECT compliance_id, statutory_provision, case when ifnull(document_name,'') = '' then trim(compliance_task) else trim(Concat_ws(' - ',document_name, compliance_task)) end AS compliance_task, compliance_description, is_active from tbl_compliances"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Task[d["compliance_task"]] = d

    def get_compliance_description(self):
        query = "SELECT compliance_id, statutory_provision, compliance_task, compliance_description, is_active from tbl_compliances"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Description[d["compliance_description"]] = d

    def get_compliance_frequency(self):
        query = "select frequency_id, frequency from tbl_compliance_frequency"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Compliance_Frequency[d["frequency"]] = d

    def get_assignee(self):
        query = "SELECT Distinct assignee as ID, employee_code, employee_name, " + \
                " CONCAT_WS(' - ', employee_code, employee_name) As Assignee " + \
                " FROM tbl_assign_compliances ac INNER JOIN tbl_users u ON (ac.assignee = u.user_id)"
        rows = self._source_db.select_all(query)
        for d in rows:
            self.Assignee[d["Assignee"]] = d

    def check_base(self, check_status, store, key_name, status_name):
        # print"store>>>", store
        # print"key_name>>>", key_name
        data = store.get(key_name)
        # print "data>>>", data
        if data is None:
            return "Not found"

        if check_status is True :
            if status_name is None :
                if data.get("is_active") == 0 :
                    return "Status Inactive"
            elif status_name == "is_closed" :
                if data.get("is_closed") == 0 :
                    return "Status Inactive"

        return True

    # def check_client_group(self, group_name):
    #     return self.check_base(True, self.Client_Group, group_name, None)

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(True, self.Legal_Entity, legal_entity_name, None)

    def check_domain(self, domain_name):
        return self.check_base(True, self.Domain, domain_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(True, self.Unit_Code, unit_code, None)

    def check_unit_name(self, unit_name):
        return self.check_base(True, self.Unit_Name, unit_name, None)

    def check_primary_legislation(self, statutories):
        return self.check_base(False, self.Statutories, statutories, None)

    def check_compliance_task(self, compliance_task):
        return self.check_base(True, self.Compliance_Task, compliance_task, None)

    def check_compliance_description(self, compliance_description):
        return self.check_base(True, self.Compliance_Description, compliance_description, None)

    def check_frequency(self, frequency):
        return self.check_base(False, self.Compliance_Frequency, frequency, None)

    def check_assignee(self, assignee):
        return self.check_base(False, self.Assignee, assignee, None)

    def is_two_levels_of_approval(_source_db):
        query = "SELECT two_levels_of_approval FROM tbl_reminder_settings"
        rows = _source_db.select_all(query)
        return bool(rows[0]["two_levels_of_approval"])

    def save_completed_task_data(self, data, legal_entity_id, session_user):
        print "save_completed_task_data>legal_entity_id>>", legal_entity_id
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
        print "before>for>columns>", columns
        for idx, d in enumerate(data):
            self.connect_source_db(legal_entity_id)
            print "for>columns>>", columns
            print "data>>>", data
            print"d>>>", d

            columns = [
            "legal_entity_id", "unit_id", "compliance_id", "start_date",
            "due_date", "completion_date", "completed_by",
            "completed_on",
            "approve_status", "approved_by", "approved_on", "current_status"
            ]

            # print "cName>>>", cName

            # Compliance ID
            cName = [d["compliance_task_name"], d["compliance_task_name"], d["compliance_description"]]
            # q = " SELECT compliance_id FROM tbl_compliances where compliance_task = TRIM(%s) AND compliance_description = TRIM(%s) LIMIT 1"
            q = "SELECT compliance_id FROM tbl_compliances where " + \
                " case when document_name = '' then compliance_task = TRIM(%s) " + \
                " else concat(document_name,' - ',compliance_task) = " + \
                " TRIM(%s) end AND compliance_description = TRIM(%s) LIMIT 1 "


            compliance_id = self._source_db.select_all(q, cName)
            compliance_id = compliance_id[0]["compliance_id"]

            completion_date = d["completion_date"]
            print "completion_date>>", completion_date

            # Unit ID
            unitCode = [d["unit_code"]]
            q = "select unit_id from tbl_units where unit_code = TRIM(%s)"
            unit_id = self._source_db.select_all(q, unitCode)
            unit_id = unit_id[0]["unit_id"]
            print "unit_id>>", unit_id

            # assignee_id
            assignee = [d["assignee"]]
            q = " SELECT distinct ac.assignee as ID, u.employee_code, " + \
                " u.employee_name, " + \
                " CONCAT_WS(' - ', u.employee_code, u.employee_name) As Assignee " + \
                " FROM tbl_assign_compliances ac INNER JOIN tbl_users u " + \
                " ON (ac.assignee = u.user_id) where " + \
                " CONCAT_WS(' - ', u.employee_code, u.employee_name)=TRIM(%s)"
            assignee_id = self._source_db.select_all(q, assignee)
            assignee_id = assignee_id[0]["ID"]
            print "assignee_id>>", assignee_id

            #Check two level of approval
            query = "SELECT two_levels_of_approval FROM tbl_reminder_settings"
            rows = self._source_db.select_all(query)
            print "rows[0][two_levels_of_approval]", rows[0]["two_levels_of_approval"]
            if int(rows[0]["two_levels_of_approval"]) == 1:
                is_two_level = True
            else:
                is_two_level = False

            print "is_two_level>>", is_two_level

            # Getting Approval and Concurrence Persons
            concur_approve_columns = "approval_person, country_id, domain_id"
            if is_two_level:
                concur_approve_columns += ", concurrence_person"
            condition = "compliance_id = %s and unit_id = %s "
            tblAssignCompliances = "tbl_assign_compliances"
            print "compliance_id>>", compliance_id
            print "unit_id>>", unit_id
            rows = self._source_db.get_data(
                tblAssignCompliances,
                concur_approve_columns,
                condition, [compliance_id, unit_id]
            )
            concurred_by = 0
            approved_by = 0
            if rows:
                approved_by = rows[0]["approval_person"]
                country_id = rows[0]["country_id"]
                domain_id = rows[0]["domain_id"]
                users = [assignee_id, approved_by]
                if is_two_level:
                    concurred_by = rows[0]["concurrence_person"]
                    users.append(concurred_by)


            # print "concurred_by>>", concurred_by
            # print "approved_by>>", approved_by
            print "Columns>1>>", columns

            print "d[document_name]>>", d["document_name"]

            #  d["document_name"]
            values = [
                legal_entity_id, unit_id, compliance_id, get_date_time(),
                d["due_date"], completion_date,
                assignee_id, completion_date,
                1, approved_by, completion_date, 3]

            print "values>1>>", values

            if d["document_name"] != "" :
                columns.append("documents")
                values.append(d["document_name"])

            if is_two_level:
                columns.append("concurrence_status")
                columns.append("concurred_by")
                columns.append("concurred_on")
                values.append(1)
                values.append(concurred_by)
                values.append(completion_date)

            print "Columns>>", columns
            print "values>>", values

            if values :
                print "columns>3>>", columns
                print "values>3>>", values
                print "self._source_db>>", self._source_db
                self._source_db.insert("tbl_compliance_history", columns, values)
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
            # "Secondary_Legislation": self.get_secondary_legislation,
            "Compliance_Task": self.check_compliance_task,
            "Compliance_Description": self.check_compliance_description,
            "Compliance_Frequency": self.check_frequency,
            "Assignee": self.check_assignee,
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
            "duplicate_error" : 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0
        }

    def compare_csv_columns(self):
        res = collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)
        if res is False :
            raise ValueError("Csv column mismatched")
    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''


    def perform_validation(self, legal_entity_id):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        self.compare_csv_columns()
        # print "perform_validation>legal_entity_id>>", legal_entity_id
        self.init_values(legal_entity_id)

        def make_error_desc(res, msg):
            if res is True :
                res = []
            if res is not True :
                if type(msg) is list:
                    res.extend(msg)
                else :
                    res.append(msg)
            return res

        for row_idx, data in enumerate(self._source_data):
            # print "completedtaskcurrentyearvalidation.py>data>>>", data
            # print "completedtaskcurrentyearvalidation.py>self._source_data>>>", self._source_data

            if row_idx == 0:
                # print "data.get(Legal_Entity)>>", data.get("Legal_Entity")
                self._legal_entity_names = data.get("Legal_Entity")
                self._Domains = data.get("Domain")
                # self._Unit_Codes = data.get("Unit_Code")
                # self._Unit_Names = data.get("Unit_Name")
                # self._Primary_Legislations = data.get("Primary_Legislation")
                # self._Secondary_Legislations = data.get("Secondary_Legislation")
                # self._Compliance_Tasks = data.get("Compliance_Task")
                # self._Compliance_Descriptions = data.get("Compliance_Description")
                # self._Compliance_Frequencys = data.get("Compliance_Frequency")
                # self._Statutory_Dates = data.get("Statutory_Date")
                # self._Due_Dates = data.get("Due_Date")
                # self._Assignees = data.get("Assignee")
                # self._Completion_Dates = data.get("Completion_Date")
                # self._Document_Names = data.get("Document_Name")

            res = True
            error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
            for key in self._csv_column_name:
                # print "_csv_column_name>key>>", key
                value = data.get(key)
                # print "_csv_column_name>value>>", value
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)

                if (key == "Document_Name" and value != '') :
                    self._doc_names.append(value)

                for v in [v.strip() for v in values] :
                    valid_failed, error_cnt = parse_csv_dictionary_values(key, v)
                    if valid_failed is not True :
                        if res is True :
                            res = valid_failed
                            error_count = error_cnt
                        else :
                            res.extend(valid_failed)
                            error_count["mandatory"] += error_cnt["mandatory"]
                            error_count["max_length"] += error_cnt["max_length"]
                            error_count["invalid_char"] += error_cnt["invalid_char"]

                    if v != "":
                        # print "unboundMethod>>before IF"
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            # print "unboundMethod>key>>", key
                            # print "unboundMethod>>", unboundMethod

                            if unboundMethod is not None :
                                isFound = unboundMethod(v)

                            if isFound is not True and isFound != "" :
                                msg = "%s - %s" % (key, isFound)
                                if res is not True :
                                    res.append(msg)
                                else :
                                    res = [msg]
                                print res
                                if "Status" in isFound :
                                    self._error_summary["inactive_error"] += 1
                                else :
                                    self._error_summary["invalid_data_error"] += 1

                if key is "Document_Name":
                    msg = []
                    if data["Document_Name"] != "":
                        file_extension = os.path.splitext(data["Document_Name"])
                        allowed_file_formats = [".pdf", ".doc", ".docx",
                                                    ".xls", ".xlsx"]
                        if file_extension[1] not in allowed_file_formats:
                            msg.append("Document Name - Invalid File Format")
                            self._error_summary["invalid_data_error"] += 1
                            res = make_error_desc(res, msg)

            if res is not True :
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else :
                    error_list.extend(res)
                res = True

                mapped_error_dict[row_idx] = error_list

                head_idx = mapped_header_dict.get(key)
                if head_idx is None :
                    head_idx = [row_idx]
                else :
                    head_idx.append(row_idx)

                mapped_header_dict[key] = head_idx
                invalid += 1
                self._error_summary["mandatory_error"] += error_count["mandatory"]
                self._error_summary["max_length_error"] += error_count["max_length"]
                self._error_summary["invalid_char_error"] += error_count["invalid_char"]

        if invalid > 0 :
            return self.make_invalid_return(mapped_error_dict, mapped_header_dict)
        else :
            return self.make_valid_return(mapped_error_dict, mapped_header_dict)

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        fileString = self._csv_name.split('.')
        file_name = "%s_%s.%s" % (
            fileString[0], "invalid", "xlsx"
        )
        final_hearder = self._csv_header
        final_hearder.append("Error Description")
        write_data_to_excel(
            os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"), file_name, final_hearder,
            self._source_data, mapped_error_dict, mapped_header_dict, self._sheet_name
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
            "doc_count": len(set(self._doc_names))
        }


    def make_valid_return(self, mapped_error_dict, mapped_header_dict):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        print "make_valid_return>list(set(self._doc_names))>>", list(set(self._doc_names))
        return {
            "return_status": True,
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "doc_names": list(set(self._doc_names)),
        }


class ValidateCompletedTaskForSubmit(SourceDB):
    def __init__(self, db, csv_id, dataResult, session_user):
        SourceDB.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._session_user_obj = session_user
        self._source_data = dataResult
        # self._declined_row_idx = []
        # self._legal_entity = None
        # self._client_group = None
        # self._csv_name = None
        # self._unit_id = None

    # def get_source_data(self):
    #     self._source_data = self._db.call_proc(
    #         "sp_assign_statutory_by_csvid", [self._csv_id]
    #     )

    def frame_data_for_main_db_insert(self, db, dataResult, legal_entity_id, session_user):
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
        print "frame_data_for_main_db_insert>legal_entity_id>>", legal_entity_id
        return self.save_completed_task_data(dataResult, legal_entity_id, session_user)
