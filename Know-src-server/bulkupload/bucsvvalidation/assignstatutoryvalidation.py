
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
from keyvalidationsettings import csv_params, parse_csv_dictionary_values, csv_params_as, parse_csv_dictionary_values_as
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)
from server.common import (
    get_date_time
)

__all__ = [
    "ValidateAssignStatutoryCsvData",
    "ValidateAssignStatutoryForApprove"
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
        self.Client_Group = {}
        self.Legal_Entity = {}
        self.Domain = {}
        self.Unit_Location = {}
        self.Unit_Code = {}
        self.Unit_Name = {}
        self.Statutories = {}
        self.Statutory_Provision = {}
        self.Compliance_Task = {}
        self.Compliance_Description = {}
        self.Organisation = {}
        self.connect_source_db()
        self._validation_method_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()

    def connect_source_db(self):
        self._source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME,
            password=KNOWLEDGE_DB_PASSWORD,
            host=KNOWLEDGE_DB_HOST,
            database=KNOWLEDGE_DATABASE_NAME,
            port=KNOWLEDGE_DB_PORT,
            autocommit=False,
        )
        self._source_db = Database(self._source_db_con)
        self._source_db.begin()

    def close_source_db(self):
        self._source_db.close()
        self.__source_db_con.close()

    def init_values(self, user_id, client_id):
        self.get_client_groups(user_id)
        self.get_legal_entities(user_id, client_id)
        self.get_domains(user_id)
        self.get_unit_location()
        self.get_unit_code(client_id)
        self.get_unit_name(client_id)
        self.get_statutories()
        self.get_statutory_provision()
        self.get_compliance_task()
        self.get_compliance_description()
        self.get_organisation()

    def get_client_groups(self, user_id):
        data = self._source_db.call_proc("sp_bu_as_user_groups", [user_id])
        for d in data :
            self.Client_Group[d["group_name"]] = d

    def get_legal_entities(self, user_id, client_id):
        data = self._source_db.call_proc("sp_bu_as_user_legal_entities", [client_id, user_id])
        for d in data :
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_domains(self, user_id):
        data = self._source_db.call_proc("sp_bu_as_user_domains", [user_id])
        for d in data :
            self.Domain[d["domain_name"]] = d

    def get_unit_location(self):
        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data :
            self.Unit_Location[d["geography_name"]] = d

    def get_unit_code(self, client_id):
        data = self._source_db.call_proc("sp_bu_unit_code_and_name", [client_id])
        for d in data:
            self.Unit_Code[d["unit_code"]] = d

    def get_unit_name(self, client_id):
        data = self._source_db.call_proc("sp_bu_unit_code_and_name", [client_id])
        for d in data:
            self.Unit_Name[d["unit_name"]] = d

    def get_statutories(self):
        data = self._source_db.call_proc("sp_bu_level_one_statutories")
        for d in data :
            self.Statutories[d["statutory_name"]] = d

    def get_statutory_provision(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data :
            self.Statutory_Provision[d["statutory_provision"]] = d

    def get_compliance_task(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data :
            self.Compliance_Task[d["compliance_task"]] = d

    def get_compliance_description(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data :
            self.Compliance_Description[d["compliance_description"]] = d

    def get_organisation(self):
        data = self._source_db.call_proc("sp_bu_organization_all")
        for d in data :
            self.Organisation[d["organisation_name"]] = d

    def check_base(self, check_status, store, key_name, status_name):
        data = store.get(key_name)
        if data is None:
            return "Not found"

        if check_status is True :
            if status_name is None :
                if data.get("is_active") == 0 :
                    return "Status Inactive"
            # elif status_name == "domain_is_active" :
            #     if data.get("domain_is_active") == 0 :
            #         return "Status Inactive"
            # elif status_name == "organization_is_active" :
            #     if data.get("organization_is_active") == 0 :
            #         return "Status Inactive"

        return True

    def check_client_group(self, group_name):
        return self.check_base(True, self.Client_Group, group_name, None)

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(True, self.Legal_Entity, legal_entity_name, None)

    def check_domain(self, domain_name):
        return self.check_base(True, self.Domain, domain_name, None)

    def check_unit_location(self, geography_name):
        return self.check_base(True, self.Unit_Location, geography_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(False, self.Unit_Code, unit_code, None)

    def check_unit_name(self, unit_name):
        return self.check_base(False, self.Unit_Name, unit_name, None)

    def check_statutories(self, statutories):
        return self.check_base(False, self.Statutories, statutories, None)

    def check_statutory_provision(self, statutory_provision):
        return self.check_base(False, self.Statutory_Provision, statutory_provision, None)

    def check_compliance_task(self, compliance_task):
        return self.check_base(False, self.Compliance_Task, compliance_task, None)

    def check_compliance_description(self, compliance_description):
        return self.check_base(False, self.Compliance_Description, compliance_description, None)

    def check_organisation(self, organisation_name):
        return self.check_base(False, self.Organisation, organisation_name, None)

    def save_client_statutories_data(self, cl_id, u_id, d_id, uploadedby):
        created_on = get_date_time()
        client_statutory_value = [
            int(cl_id), int(u_id),
            int(d_id),
            int(uploadedby), str(created_on)
        ]
        q = "INSERT INTO tbl_client_statutories (client_id, unit_id, domain_id, " + \
            " approved_by, approved_on) values " + \
            " (%s, %s, %s, %s, %s)"
        client_statutory_id = self._source_db.execute_insert(
            q, client_statutory_value
        )
        # self._source_db.commit()
        if client_statutory_id is False:
            raise process_error("E018")
        return client_statutory_id

    def save_client_compliances_data(self, cl_id, le_id, u_id, d_id, cs_id, data):
        created_on = get_date_time()
        columns = [
            "client_statutory_id",
            "client_id", "legal_entity_id", "unit_id",
            "domain_id", "statutory_id", "statutory_applicable_status",
            "remarks", "compliance_id", "compliance_applicable_status",
            "is_approved", "approved_by", "approved_on",
            "updated_by", "updated_on"

        ]
        values = []
        for idx, d in enumerate(data) :
            statu_id = self.Statutories.get(d["Primary_Legislation"]).get("statutory_id")
            comp_id = None
            c_ids = self._source_db.call_proc("sp_bu_get_compliance_id_by_name" , [d["Compliance_Task"], d["Compliance_Description"]])
            for c_id in c_ids :
                comp_id = c_id["compliance_id"]

            values.append((
                int(cs_id), cl_id, le_id, u_id, d_id, statu_id, 
                d["Statutory_Applicable_Status"], 
                d["Statutory_remarks"], comp_id,
                d["Compliance_Applicable_Status"], 
                1, d["uploaded_by"], created_on, 
                d["uploaded_by"], created_on
            ))

        if values :
            self._source_db.bulk_insert("tbl_client_compliances", columns, values)
            # self._source_db.commit()
            return True
        else :
            return False

    # main db related validation mapped with field name
    def statusCheckMethods(self):
        self._validation_method_maps = {
            "Client_Group": self.check_client_group,
            "Legal_Entity": self.check_legal_entity,
            "Domain": self.check_domain,
            "Unit_Location": self.check_unit_location,
            "Unit_Code": self.check_unit_code,
            "Unit_Name": self.check_unit_name,
            "Primary_Legislation": self.check_statutories,
            "Statutory_Provision": self.check_statutory_provision,
            "Compliance_Task": self.check_compliance_task,
            "Compliance_Description": self.check_compliance_description,
            "Organisation": self.check_organisation
        }

    def csv_column_fields(self):
        self._csv_column_name = [
            "S.No", "Client_Group" ,"Legal_Entity", "Domain",
            "Organisation", "Unit_Code", "Unit_Name",
            "Unit_Location", "Primary_Legislation", "Secondary_Legislaion", 
            "Statutory_Provision", "Compliance_Task",
            "Compliance_Description", "Statutory_Applicable_Status",
            "Statutory_remarks", "Compliance_Applicable_Status"
        ]

    def source_commit(self):
        self._source_db.commit()
        
class ValidateAssignStatutoryCsvData(SourceDB):
    def __init__(self, db, source_data, session_user, csv_name, csv_header, client_id):
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._client_id = client_id
        self._error_summary = {}
        self.errorSummary()

        self._sheet_name = "Assign Statutory"

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
            raise ValueError("Invalid Csv file")
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
        self.init_values(self._session_user_obj.user_id(), self._client_id)

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
            res = True
            error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
            for key in self._csv_column_name:
                
                value = data.get(key)
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params_as.get(key)

                for v in [v.strip() for v in values] :
                    valid_failed, error_cnt = parse_csv_dictionary_values_as(key, v)
                    if valid_failed is not True :
                        if res is True :
                            res = valid_failed
                            error_count = error_cnt
                        else :
                            res.extend(valid_failed)
                            error_count["mandatory"] += error_cnt["mandatory"]
                            error_count["max_length"] += error_cnt["max_length"]
                            error_count["invalid_char"] += error_cnt["invalid_char"]

                    if v != "" :
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
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
        # rename_file_type(file_name, "txt")
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

class ValidateAssignStatutoryForApprove(SourceDB):
    def __init__(self, db, csv_id, client_id, legal_entity_id, session_user):
        SourceDB.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._client_id = client_id
        self._legal_entity_id = legal_entity_id
        self._session_user_obj = session_user
        self._source_data = None
        self._declined_row_idx = []
        self.get_source_data()

    def get_source_data(self):
        self._source_data = self._db.call_proc("sp_assign_statutory_by_csvid", [self._csv_id])

    def perform_validation_before_submit(self):
        declined_count = 0
        self._declined_row_idx = []
        self.init_values(self._session_user_obj.user_id(), self._client_id)

        for row_idx, data in enumerate(self._source_data):
            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                if value is None :
                    continue
                   
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params_as.get(key)
                if csvParam is None :
                    continue

                for v in values :
                    v = v.strip()

                    if v != "" :
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            if unboundMethod is not None :
                                isFound = unboundMethod(v)

                        if isFound is not True and isFound != "" :
                            declined_count += 1

            # if not self.check_compliance_task_name_duplicate(
            #     self._country_id, self._domain_id, data.get("Statutory"),
            #     data.get("Statutory_Provision"), data.get("Compliance_Task")
            # ) :
            #     print "compliance task name dulicate"
            #     declined_count += 1

            # if not self.check_task_id_duplicate(
            #     self._country_id, self._domain_id, data.get("Statutory"),
            #     data.get("Statutory_Provision"), data.get("Compliance_Task"),
            #     data.get("Task_ID")
            # ):
            #     print "Task id duplicate"
            #     declined_count += 1

            if declined_count > 0 :
                self._declined_row_idx.append(data.get("bulk_assign_statutory_id"))
        return self._declined_row_idx

    def frame_data_for_main_db_insert(self):
        self._source_data.sort(key=lambda x: (
             x["Domain"], x["Unit_Name"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"], s["Unit_Name"]
        )):
            grouped_list = list(v)
            if len(grouped_list) == 0:
                continue
            
            unit_id = None
            domain_id = None
            value = grouped_list[0]
        
            unit_id = self.Unit_Code.get(value.get("Unit_Code")).get("unit_id")
            domain_id = self.Domain.get(value.get("Domain")).get("domain_id")
            uploaded_by = value.get("uploaded_by")

            cs_id = self.save_client_statutories_data(self._client_id, unit_id, domain_id, uploaded_by)
            self.save_client_compliances_data(self._client_id, self._legal_entity_id, unit_id, domain_id, cs_id, grouped_list)

    def make_rejection(self, declined_info):
        q = "update tbl_bulk_assign_statutory set action = 3 where bulk_assign_statutory_id in %s"
        self._source_db.execute_insert(q, [",".join(declined_info)])
