import os
import collections
import mysql.connector
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH
)



from client_keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..client_bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)
from server.common import (
    get_date_time
)



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
        self.connect_source_db()
        self._validation_method_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()

    def connect_source_db(self):
        # print "API.bulk_db_connect", bulk_db_connect
        # print "completedtaskcurrentyearvalidation>user>>", BULK_LE_DB_CONNECT["db_username"]
        # print "completedtaskcurrentyearvalidation>password>>", BULK_LE_DB_CONNECT["db_password"]
        # print "completedtaskcurrentyearvalidation>host>>", BULK_LE_DB_CONNECT["ip_address"]
        # print "completedtaskcurrentyearvalidation>database>>", BULK_LE_DB_CONNECT["db_name"]
        # print "completedtaskcurrentyearvalidation>port>>", BULK_LE_DB_CONNECT["db_ip.port"]

        self._source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database="compfie_le_att_1",
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        self._source_db = Database(self._source_db_con)
        self._source_db.begin()

    def close_source_db(self):
        self._source_db.close()
        self.__source_db_con.close()

    def init_values(self):
        print "init_values(self)>>>>"
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
        print"store>>>", store
        print"key_name>>>", key_name
        data = store.get(key_name)
        print "data>>>", data
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


    def save_completed_task_data(self, data):
        # created_on = get_date_time()
        # columns = [
        #     "client_statutory_id",
        #     "client_id", "legal_entity_id", "unit_id",
        #     "domain_id", "statutory_id", "statutory_applicable_status",
        #     "remarks", "compliance_id", "compliance_applicable_status",
        #     "is_approved", "approved_by", "approved_on",
        #     "updated_by", "updated_on"
        # ]
        columns = [
            "legal_entity_id", "unit_id", "compliance_id", "start_date",
            "due_date", "completion_date", "completed_by", "approved_by"
        ]

        values = []
        for idx,d in enumerate(data):
            print "data>>>", data
            print"d>>>", d
            cName = d["compliance_task_name"]
            print "cName>>>", cName

            # q = " SELECT compliance_id FROM tbl_compliances where compliance_task like TRIM('%s') "
            q = "SELECT compliance_id, compliance_task FROM tbl_compliances LIMIT 1"
            c = self._source_db.select_all(q, cName)
            print "c>>>", c
            print"compliance_id>>", c[0]["compliance_id"]
            compliance_id = c[0]["compliance_id"]

            values.append((
                "1", "1", compliance_id,
                d["due_date"], d["due_date"], d["due_date"],
                "1","1"
            ))
            # values.append((
            #     "1", "1", "1",
            #     d["due_date"], d["due_date"], d["due_date"],
            #     "1","1"
            # ))

        if values :
            self._source_db.bulk_insert("tbl_compliance_history", columns, values)
            self._source_db.commit()
            return True
        else :
            return False



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


    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        self.compare_csv_columns()
        self.init_values()

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
            print "completedtaskcurrentyearvalidation.py>data>>>", data
            print "completedtaskcurrentyearvalidation.py>self._source_data>>>", self._source_data

            if row_idx == 0:
                print "data.get(Legal_Entity)>>", data.get("Legal_Entity")
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
                print "_csv_column_name>key>>", key
                value = data.get(key)
                print "_csv_column_name>value>>", value
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)

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
                        print "unboundMethod>>before IF"
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            print "unboundMethod>key>>", key
                            print "unboundMethod>>", unboundMethod

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
            "invalid": invalid
        }


    def make_valid_return(self, mapped_error_dict, mapped_header_dict):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        return {
            "return_status": True,
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid
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

    def frame_data_for_main_db_insert(self, db, dataResult):
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
        return self.save_completed_task_data(dataResult)
