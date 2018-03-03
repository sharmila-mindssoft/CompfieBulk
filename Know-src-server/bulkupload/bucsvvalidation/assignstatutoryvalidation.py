
import os
import collections
import mysql.connector

from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH

)

from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)

__all__ = [
    "ValidateAssignStatutoryCsvData"
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
        self.Legal_Entity = {}
        self.Unit_Location = {}
        self.Unit_Code = {}
        self.connect_source_db()


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
        self.get_legal_entities(user_id, client_id)
        self.get_unit_location()
        self.get_unit_code(client_id)

    def get_legal_entities(self, user_id, client_id):
        data = self._source_db.call_proc("sp_bu_as_user_legal_entities", [client_id, user_id])
        for d in data :
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_unit_location(self):
        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data :
            self.Unit_Location[d["parent_names"]] = d

    def get_unit_code(self, client_id):
        data = self._source_db.call_proc("sp_bu_unit_code", [client_id])
        for d in data:
            self.Unit_Code[d["unit_code"]] = d


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

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(True, self.Legal_Entity, legal_entity_name, None)

    def check_unit_location(self, geography_name):
        return self.check_base(True, self.Unit_Location, geography_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(False, self.Unit_Code, unit_code, None)


class ValidateAssignStatutoryCsvData(SourceDB):
    def __init__(self, db, source_data, session_user, csv_name, csv_header, client_id):
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._client_id = client_id

        self._validation_method_maps = {}
        self._error_summary = {}
        self.errorSummary()
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()
        self._sheet_name = "Assign Statutory"

    # main db related validation mapped with field name
    def statusCheckMethods(self):
        self._validation_method_maps = {
            "Legal_Entity": self.check_legal_entity,
            "Unit_Location": self.check_unit_location,
            "Unit_Code": self.check_unit_code
            
        }

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

    def csv_column_fields(self):
        self._csv_column_name = [
            "S.No", "Client_Group" ,"Legal_Entity", "Domain",
            "Organisation", "Unit_Code", "Unit_Name",
            "Unit_Location", "Primary_Legislation", "Secondary_Legislaion", 
            "Statutory_Provision", "Compliance_Task",
            "Compliance_Description", "Statutory_Applicable_Status",
            "Statutory_remarks", "Compliance_Applicable_Status"
        ]

    def compare_csv_columns(self):
        return collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)

    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''
    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        isValid = True
        self.init_values(self._session_user_obj.user_id(), self._client_id)
        if self.compare_csv_columns() is False :
            raise ValueError("Csv Column Mismatched")

        for row_idx, data in enumerate(self._source_data):

            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)
                res = True
                error_count = {
                    "mandatory": 0,
                    "max_length": 0,
                    "invalid_char": 0
                }
                # if (key == "Format" and value != ''):
                #     self._doc_names.append(value)
                for v in values :
                    v = v.strip()
                    valid_failed, error_cnt = parse_csv_dictionary_values(key, v)
                    if valid_failed is not True :
                        res = valid_failed
                        error_count = error_cnt
                    if v != "" :
                        if csvParam.get("check_is_exists") is True or csvParam.get("check_is_active") is True :
                            unboundMethod = self._validation_method_maps.get(key)
                            if unboundMethod is not None :
                                isFound = unboundMethod(v)
                            
                        if isFound is not True and isFound != "" :
                            if valid_failed is not True :
                                valid_failed.append(key + ' - ' + isFound)
                            else :
                                valid_failed = [key + ' - ' + isFound]
                            res = valid_failed

                            if "Status" in isFound :
                                self._error_summary["inactive_error"] += 1
                            else :
                                self._error_summary["invalid_data_error"] += 1

                if res is not True :
                    # mapped_error_dict[row_idx] = CSV_DELIMITER.join(res)
                    error_list = mapped_error_dict.get(row_idx)

                    if error_list is None:
                        error_list = res
                    else :
                        error_list.extend(res)
                    mapped_error_dict[row_idx] = error_list

                    head_idx = mapped_header_dict.get(key)
                    if head_idx is None :
                        head_idx = [row_idx]
                    else :
                        head_idx.append(row_idx)
                    mapped_header_dict[key] = head_idx
                    isValid = False
                    self._error_summary["mandatory_error"] += error_count["mandatory"]
                    self._error_summary["max_length_error"] += error_count["max_length"]
                    self._error_summary["invalid_char_error"] += error_count["invalid_char"]

        if isValid is False :
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
