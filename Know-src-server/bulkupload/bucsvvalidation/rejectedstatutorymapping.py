import os
import collections
import mysql.connector

import pyexcel.ext.xlsx
import pyexcel.ext.xls

from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, REJECTED_DOWNLOAD_PATH, REJECTED_DOWNLOAD_BASE_PATH
)

from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type, rename_download_file_type
)

__all__ = [
    "ValidateRejectedSMBulkCsvData"
]
################################
'''
    csv data validation
    param:
        csv_data :

'''
################################

# class SourceDB(object):
#     def __init__(self):
#         self._source_db = None
#         self._source_db_con = None
#         self.approve_status = {}
#         self.Rejected_On = {}
#         self.Rejected_By = {}
#         self.No_Of_Records = {}
#         self.Declined_Count = {}
#         self.Rejected_File = {}
#         self.Reason_For_Rejection = {}

#         self.connect_source_db()

#     def connect_source_db(self):
#         self._source_db_con = mysql.connector.connect(
#             user=KNOWLEDGE_DB_USERNAME,
#             password=KNOWLEDGE_DB_PASSWORD,
#             host=KNOWLEDGE_DB_HOST,
#             database=KNOWLEDGE_DATABASE_NAME,
#             port=KNOWLEDGE_DB_PORT,
#             autocommit=False,
#         )
#         self._source_db = Database(self._source_db_con)
#         self._source_db.begin()

#     def close_source_db(self):
#         self._source_db.close()
#         self._source_db_con.close()

#     def init_values(self, user_id, client_id):
#         self.get_legal_entities(user_id, client_id)
#         self.get_divisions(client_id)
#         self.get_categories(client_id)
#         self.get_geography_level(user_id)
#         self.get_unit_location()
#         self.get_unit_code(client_id)
#         self.get_domains_organizations(client_id)

#     def get_legal_entities(self, user_id, client_id):
#         data = self._source_db.call_proc_with_multiresult_set("sp_bu_legal_entities", [client_id, user_id], 2)
#         for d in data[1] :
#             self.approve_status[d["legal_entity_name"]] = d

#     def get_divisions(self, client_id):
#         data = self._source_db.call_proc("sp_bu_divisions", [client_id])
#         for d in data :
#             self.Rejected_On[d["division_name"]] = d

#     def get_categories(self, client_id):
#         data = self._source_db.call_proc("sp_bu_categories", [client_id])
#         for d in data :
#             self.Rejected_By[d["category_name"]] = d

#     def get_geography_level(self, user_id):
#         data = self._source_db.call_proc("sp_bu_geography_levels", [user_id])
#         for d in data :
#             self.No_Of_Records	[d["level_name"]] = d

#     def get_unit_location(self):
#         data = self._source_db.call_proc("sp_bu_client_unit_geographies")
#         for d in data :
#             self.Declined_Count[d["parent_names"]] = d

#     def get_unit_code(self, client_id):
#         data = self._source_db.call_proc("sp_bu_unit_code", [client_id])
#         for d in data:
#             self.Rejected_File[d["unit_code"]] = d

#     # def get_domains_organizations(self, client_id):
#     #     data = self._source_db.call_proc("sp_bu_domains_organization_unit_count", [client_id])
#     #     for d in data:
#     #         self.Reason_For_Rejection[d["domain_name"]] = d
#     #         self.Organization[d["organization_name"]] = d

#     def check_base(self, check_status, store, key_name, status_name):
#         data = store.get(key_name)

#         if data is None:
#             return "Not found"

#         if check_status is True :
#             if status_name is None :
#                 if data.get("is_active") == 0 :
#                     return "Status Inactive"
#             elif status_name == "domain_is_active" :
#                 if data.get("domain_is_active") == 0 :
#                     return "Status Inactive"
#             elif status_name == "organization_is_active" :
#                 if data.get("organization_is_active") == 0 :
#                     return "Status Inactive"

#         return True

#     def check_legal_entity(self, legal_entity_name):
#         return self.check_base(
#             True, self.approve_status, legal_entity_name, None)

#     def check_division(self, division_name):
#         return self.check_base(False, self.Rejected_On, division_name, None)

#     def check_category(self, category_name):
#         return self.check_base(False, self.Rejected_By, category_name, None)

#     def check_geography_level(self, level_name):
#         return self.check_base(True, self.No_Of_Records	, level_name, None)

#     def check_unit_location(self, geography_name):
#         return self.check_base(True, self.Declined_Count, geography_name, None)

#     def check_unit_code(self, unit_code):
#         return self.check_base(False, self.Rejected_File, unit_code, None)

#     def check_domain(self, domain_name):
#         return self.check_base(True, self.Reason_For_Rejection, domain_name, "domain_is_active")

#     # def check_organization(self, organization_name):
#     #     return self.check_base(True, self.Organization, organization_name, "organization_is_active")


# db, source_data, session_user, country_id,
#         domain_id, csv_id, download_format

class ValidateRejectedSMBulkCsvData():
    def __init__(self, db, source_data, session_user, download_format, csv_name, csv_header):
        # super(SourceDB, self).__init__()
        # SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._download_format = download_format
        self._validation_method_maps = {}
        self._error_summary = {}
        # self.errorSummary()
        # self.statusCheckMethods()
        self._csv_column_name = []
        self._csv_column_header=[]
        self.csv_column_fields()
        self._doc_names = []
        self._sheet_name = "Rejected StatutoryMapping"

    def csv_column_fields(self):
        self._csv_column_name = self._csv_header

    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        download_format = self._download_format
        isValid = True

        for row_idx, data in enumerate(self._source_data):
            for key in self._csv_column_name:
                value = data.get(key)
                return self.generateDownloadFiles(mapped_error_dict, mapped_header_dict, download_format)

    def generateDownloadFiles(self, mapped_error_dict, mapped_header_dict, download_format):

        fileString = self._csv_name.split('.')
        file_txt_name=fileString[0]
        file_name = "%s_%s.%s" % (
            fileString[0], "download", "xlsx"
        )
        final_hearder = self._csv_column_name
        invalid = len(mapped_error_dict.keys())
        total = len(self._source_data)

        # if(download_format=="xlsx"):

        write_data_to_excel(
            os.path.join(REJECTED_DOWNLOAD_PATH, "xlsx"), file_name, final_hearder,
            self._source_data, mapped_error_dict, mapped_header_dict, self._sheet_name
        )
        xlsx_download_path=REJECTED_DOWNLOAD_BASE_PATH+"xlsx/"
        xlsx_link = os.path.join(xlsx_download_path, file_name)

        csv_link=rename_download_file_type(file_name, "csv")

        ods_link=rename_download_file_type(file_name, "ods")

        txt_file_name = "%s_%s.%s" % (
            fileString[0], "download", "txt"
        )
        txt_link = os.path.join(
             REJECTED_DOWNLOAD_BASE_PATH, txt_file_name)

        return {
            "xlsx_link": xlsx_link,
            "csv_link" : csv_link,
            "ods_link" : ods_link,
            "txt_link" : txt_link

        }
