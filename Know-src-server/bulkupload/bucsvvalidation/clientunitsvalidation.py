import os
import mysql.connector

from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH

)

from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    write_data_to_excel, uuid, rename_file_type
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
    def __init__(self, session_user):
        self._source_db = None
        self._source_db_con = None
        self.Legal_Entity = {}

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

    def init_values(self, client_id):
        self.get_legal_entities(client_id)

    def get_legal_entities(self, client_id):
        data = self._source_db.call_proc("sp_bu_legal_entities", [client_id])
        for d in data :
            self.Legal_Entity[d["legal_entity_name"]] = d

    def check_base(self, check_status, store, key_name):
        data = store.get(key_name)

        if data is None:
            return "Not found"

        if check_status is True :
            if data.get("is_active") == 0 :
                return "Status Inactive"

        return True

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(True, self.Legal_Entity, legal_entity_name)


class ValidateClientUnitsBulkCsvData(SourceDB):
    def __init__(self, db, source_data, session_user, client_id, csv_name, csv_header):
        super(SourceDB, self).__init__(session_user)
        self._db = db
        self._source_data = source_data
        self._client_id = client_id
        self._csv_name = csv_name
        self._csv_header = csv_header
        self.init_values(client_id)
        self._validation_method_maps = {}
        self._error_summary = {}
        self.statusCheckMethods()

    def statusCheckMethods(self):
        self._validation_method_maps = {
            "Legal_Entity": self.check_legal_entity
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

    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        isValid = True
        for idx, data in enumerate(self._source_data):

            for key, value in data.items() :
                csvParam = csv_params.get(key)
                print "1"
                print csvParam
                res, error_count = parse_csv_dictionary_values(key, value)
                print "3"
                print res, error_count
                if csvParam.get("isFoundCheck") is True or csvParam.get("isActiveCheck") is True :
                    isFound = self._validation_method_maps.get(key)(value)
                    print "4"
                    print isFound
                    if isFound is not True :
                        if res is not True :
                            res.append(key + ' - ' + isFound)
                        else :
                            res = [key + ' - ' + isFound]
                        if isFound.index('Status') > -1:
                            self._error_summary["inactive_error"] += 1
                        else :
                            self._error_summary["invalid_data_error"] += 1

                if res is not True :
                    mapped_error_dict[idx] = CSV_DELIMITER.join(res)
                    head_idx = mapped_header_dict.get(idx)
                    if head_idx is None :
                        head_idx = [self._csv_header.index(key)]
                    else :
                        head_idx.append(self._csv_header.index(key))
                    mapped_header_dict[idx] = head_idx
                    isValid = False

                    self._error_summary["mandatory_error"] += error_count["mandatory"]
                    self._error_summary["max_length_error"] += error_count["max_length"]
                    self._error_summary["invalid_char_error"] += error_count["invalid_char"]

        if isValid is False :
            return self.make_invalid_file(mapped_error_dict, mapped_header_dict)
        else :
            return self.make_valid_return(mapped_error_dict, mapped_header_dict)

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        file_name = "%s_%s_%s" % (
            self._csv_name, "invalid", uuid()
        )
        final_hearder = self._csv_header
        final_hearder.append("Error Description")
        write_data_to_excel(
            os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"), file_name, final_hearder,
            self._source_data, mapped_error_dict, mapped_header_dict
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
            "invali_file": file_name,
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
            "data": self._source_data,
            "total": total,
            "valid": total - invalid,
            "invalid": invalid
        }
