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
    "ValidateClientUnitsBulkCsvData"
]
################################
'''
    csv data validation
    param:
        csv_data :

'''
################################

class SourceDB(object):
    def __init__(self):
        self._source_db = None
        self._source_db_con = None
        self.Legal_Entity = {}
        self.Division = {}
        self.Category = {}
        self.Geography_Level = {}
        self.Unit_Location = {}
        self.Unit_Code = {}
        self.Domain_Organization = {}
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
        self._source_db_con.close()

    def init_values(self, user_id, client_id):
        self.get_legal_entities(user_id, client_id)
        self.get_divisions(client_id)
        self.get_categories(client_id)
        self.get_geography_level(user_id)
        self.get_unit_location()
        self.get_unit_code(client_id)
        self.get_domains_organizations(client_id)

    def get_legal_entities(self, user_id, client_id):
        data = self._source_db.call_proc_with_multiresult_set("sp_bu_legal_entities", [client_id, user_id], 2)
        for d in data[1] :
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_divisions(self, client_id):
        data = self._source_db.call_proc("sp_bu_divisions", [client_id])
        for d in data :
            self.Division[d["division_name"]] = d

    def get_categories(self, client_id):
        data = self._source_db.call_proc("sp_bu_categories", [client_id])
        for d in data :
            self.Category[d["category_name"]] = d

    def get_geography_level(self, user_id):
        data = self._source_db.call_proc("sp_bu_geography_levels", [user_id])
        for d in data :
            self.Geography_Level[d["level_name"]] = d

    def get_unit_location(self):
        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data :
            self.Unit_Location[d["parent_names"]] = d

    def get_unit_code(self, client_id):
        data = self._source_db.call_proc("sp_bu_unit_code", [client_id])
        for d in data:
            self.Unit_Code[d["unit_code"]] = d

    def get_domains_organizations(self, client_id):
        data = self._source_db.call_proc("sp_bu_domains_organization_unit_count", [client_id])
        for d in data:
            self.Unit_Code[d["legal_entity_id"]] = d

    def check_base(self, check_status, store, key_name):
        print "inside check base"
        print key_name
        data = store.get(key_name)
        print "after checking data"
        print data

        if data is None:
            return "Not found"

        if check_status is True :
            if (key_name == "domain_name"):
                if data.get("domain_is_active") == 0 :
                    return "Status Inactive"
            elif (key_name == "organization_name"):
                if data.get("organization_is_active") == 0 :
                    return "Status Inactive"
            else :
                if data.get("is_active") == 0 :
                    return "Status Inactive"

        return True

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(True, self.Legal_Entity, legal_entity_name)

    def check_division(self, division_name):
        return self.check_base(False, self.Division, division_name)

    def check_category(self, category_name):
        return self.check_base(False, self.Category, category_name)

    def check_geography_level(self, level_name):
        return self.check_base(True, self.Geography_Level, level_name)

    def check_unit_location(self, geography_name):
        return self.check_base(True, self.Unit_Location, geography_name)

    def check_unit_code(self, unit_code):
        return self.check_base(False, self.Unit_Code, unit_code)

    def check_domain(self, domain_name):
        return self.check_base(True, self.Domain_Organization, domain_name)

    def check_organization(self, organization_name):
        return self.check_base(True, self.Domain_Organization, organization_name)


class ValidateClientUnitsBulkCsvData(SourceDB):
    def __init__(self, db, source_data, session_user, client_id, csv_name, csv_header):
        # super(SourceDB, self).__init__()
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._client_id = client_id
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._validation_method_maps = {}
        self._error_summary = {}
        self.errorSummary()
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()
        self._doc_names = []
        self._sheet_name = "Client Unit"

    def statusCheckMethods(self):
        self._validation_method_maps = {
            "Legal_Entity": self.check_legal_entity,
            "Division": self.check_division,
            "Category": self.check_category,
            "Geography_Level": self.check_geography_level,
            "Unit_Location": self.check_unit_location,
            "Unit_Code": self.check_unit_code,
            "Domain": self.check_domain,
            "Organization": self.check_organization
        }

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
            "Legal_Entity", "Division", "Category", "Geography_Level",
            "Unit_Location", "Unit_Code", "Unit_Name", "Unit_Address",
            "City", "State", "Postal_Code", "Domain", "Organization"
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
                print "1"
                print value
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                print "2"
                print values
                csvParam = csv_params.get(key)
                print "3"
                print csvParam
                res = True
                error_count = {
                    "mandatory": 0,
                    "max_length": 0,
                    "invalid_char": 0
                }
                if (key == "Format" and value != ''):
                    self._doc_names.append(value)
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
                    print "self._error_summary"
                    print self._error_summary
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
            "invalid": invalid,
            "doc_count": len(set(self._doc_names))
        }

    def make_valid_return(self, mapped_error_dict, mapped_header_dict):
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)
        return {
            "return_status": True,
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid,
            "doc_count": len(set(self._doc_names)),
            "doc_names": list(set(self._doc_names))
        }
