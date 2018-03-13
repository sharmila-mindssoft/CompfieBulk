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
from server.common import (
    get_date_time
)
from server.database.forms import *
from server.database.knowledgetransaction import save_messages
from server.exceptionmessage import process_error
from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)

__all__ = [
    "ValidateClientUnitsBulkCsvData",
    "ValidateClientUnitsBulkDataForApprove"
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
        self.Domain = {}
        self.Organization = {}
        self.Legal_Entity_Id = None
        self.Business_Group_Id = None
        self.Country_Id = None
        self.Level_Id = None
        self._csv_column_name = []
        self.csv_column_fields()
        self.statusCheckMethods()
        self.connect_source_db()

    def csv_column_fields(self):
        self._csv_column_name = [
            "Legal_Entity", "Division", "Category", "Geography_Level",
            "Unit_Location", "Unit_Code", "Unit_Name", "Unit_Address",
            "City", "State", "Postal_Code", "Domain", "Organization"
        ]

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
            self.Geography_Level[str(d["country_id"]) + '-' + d["level_name"]] = d

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
            self.Domain[str(d["legal_entity_id"]) + "-" + d["domain_name"]] = d
            self.Organization[str(d["legal_entity_id"]) + "-" + d["domain_name"] + " >> " + d["organization_name"]] = d

    def check_base(self, check_status, store, key_name, status_name):
        data = store.get(key_name)

        if (data is not None and check_status is True) :
            if status_name is None :
                if data.get("is_active") == 0 :
                    return "Status Inactive"
            elif status_name == "domain_is_active" :
                if data.get("domain_is_active") == 0 :
                    return "Status Inactive"
            elif status_name == "organization_is_active" :
                if data.get("organization_is_active") == 0 :
                    return "Status Inactive"

        return True

    def check_legal_entity(self, legal_entity_name):
        store = self.Legal_Entity
        data = store.get(legal_entity_name)
        if data is not None and data.get("is_closed") == 0 and data.get("is_approved") == 1:
            self.Legal_Entity_Id = data.get("legal_entity_id")
            self.Country_Id = data.get("country_id")
            self.Business_Group_Id = data.get("business_group_id")
            return self.check_base(True, store, legal_entity_name, None)
        else:
            return "Not found"

    def check_division(self, division_name):
        store = self.Division
        data = store.get(division_name)
        if data is not None:
            return self.check_base(False, self.Division, division_name, None)
        else:
            return "Not found"

    def check_category(self, category_name):
        store = self.Category
        data = store.get(category_name)
        if data is not None:
            return self.check_base(False, self.Category, category_name, None)
        else:
            return "Not found"

    def check_geography_level(self, level_name):
        store = self.Geography_Level
        data = store.get(str(self.Country_Id) + '-' + level_name)
        if data is not None:
            if (data.get("country_id") == self.Country_Id and data.get("level_name") == level_name):
                self.Level_Id = data.get("level_id")
                return self.check_base(True, self.Geography_Level, level_name, None)
            else:
                return "Not found"
        else:
            return "Not found"

    def check_unit_location(self, geography_name):
        store = self.Unit_Location
        data = store.get(geography_name)
        if data is not None:
            if (data.get("level_id") == self.Level_Id):
                return self.check_base(True, self.Unit_Location, geography_name, None)
            else:
                return "Not found"
        else:
            return "Not found"

    def check_unit_code(self, unit_code):
        store = self.Unit_Code
        data = store.get(unit_code)
        if data is not None and unit_code != "auto_gen":
            if (data.get("legal_entity_id") == self.Legal_Entity_Id):
                return self.check_base(False, self.Unit_Code, unit_code, None)
            else:
                return "Not found"
        else:
            return "Not found"

    def check_domain(self, domain_name):
        store = self.Domain
        errDesc = ""
        status = None
        if domain_name.find(CSV_DELIMITER) > 0:
            splittedDomain = domain_name.split(CSV_DELIMITER)
            for d in splittedDomain:
                data = store.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if data is not None:
                    status = self.check_base(True, self.Domain, domain_name, "domain_is_active")
                    if status is "Status Inactive":
                        errDesc = errDesc + d + status
                else:
                    errDesc = errDesc + d + " Not Found" + ","
            if errDesc is not None:
                return errDesc
        else:
            data = store.get(str(self.Legal_Entity_Id) + "-" + domain_name)
            if data is not None:
                return self.check_base(True, self.Domain, domain_name, "domain_is_active")
            else:
                return domain_name + " Not Found"

    def check_organization(self, organization_name):
        store = self.Organization
        errDesc = ""
        status = None
        if organization_name.find(CSV_DELIMITER) > 0:
            splittedOrg = organization_name.split(CSV_DELIMITER)
            for d in splittedOrg:
                data = store.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if data is not None:
                    status = self.check_base(True, self.Organization, organization_name, "organization_is_active")
                    if status is "Status Inactive":
                        errDesc = errDesc + d + status
                    else:
                        if int(data.get("created_units")) >= int(data.get("total_unit_count")):
                            errDesc = errDesc + d + " Unit count exceeds the limit"
                else:
                    errDesc = errDesc + d + " Not Found" + ","
            if errDesc is not None:
                return errDesc
        else:
            data = store.get(str(self.Legal_Entity_Id) + "-" + organization_name)
            if data is not None:
                if int(data.get("created_units")) >= int(data.get("total_unit_count")):
                    errDesc = errDesc + d + " Unit count exceeds the limit"
                else:
                    return self.check_base(True, self.Organization, organization_name, "organization_is_active")
            else:
                return organization_name + " Not Found"

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

    def save_division(self, cl_id, le_id, bg_id, division_name, createdby):
        created_on = get_date_time()
        insert_value = [
            int(cl_id), int(le_id),
            int(bg_id), division_name,
            int(createdby), str(created_on)
        ]
        q = "INSERT INTO tbl_divisions (client_id, legal_entity_id, " + \
            " business_group_id, division_name, created_by, created_on) values " + \
            " (%s, %s, %s, %s, %s, %s)"
        division_id = self._source_db.execute_insert(
            q, insert_value
        )
        if division_id is False:
            raise process_error("E054")
        return division_id

    def save_category(self, cl_id, le_id, bg_id, division_id, category_name, createdby):
        created_on = get_date_time()
        insert_value = [
            int(cl_id), int(le_id),
            int(bg_id), int(division_id),
            category_name, int(createdby), str(created_on)
        ]
        q = "INSERT INTO tbl_categories (client_id, legal_entity_id, business_group_id, " + \
            "division_id, category_name, created_by, created_on) values " + \
            " (%s, %s, %s, %s, %s, %s, %s)"
        category_id = self._source_db.execute_insert(
            q, insert_value
        )
        if category_id is False:
            raise process_error("E093")
        return category_id

    def generate_unit_code(self, cl_id, grp_name):
        unit_code_start_letters = grp_name[:2].upper()
        select_param = [
            str(unit_code_start_letters),
            str(unit_code_start_letters),
            int(cl_id)
        ]
        q = "SELECT (max(TRIM(LEADING %s FROM unit_code))+1) as code " + \
            "FROM tbl_units WHERE unit_code like binary concat( %s,'%') and " + \
            "CHAR_LENGTH(unit_code) = 7 and client_id=%s; "
        uc = self._source_db.select_one(
            q, select_param
        )
        if uc is False:
            raise process_error("E056")
        else:
            if (uc > 0 and uc < 10):
                unit_code = str(unit_code_start_letters) + '0000' + uc
            elif (uc >= 10 and uc < 100):
                unit_code = str(unit_code_start_letters) + '000' + uc
            elif (uc >= 100 and uc < 1000):
                unit_code = str(unit_code_start_letters) + '00' + uc
            elif (uc >= 1000 and uc < 10000):
                unit_code = str(unit_code_start_letters) + '0' + uc
        return unit_code

    def save_units(self, cl_id, bg_id, le_id, division_id, category_id, country_id, geography_id, u_code, u_name, u_addr, post_code, createdby):
        created_on = get_date_time()
        insert_value = [
            int(cl_id), int(bg_id), int(le_id), int(division_id), int(category_id),
            int(country_id), int(geography_id), str(u_code), str(u_name), str(u_addr),
            str(post_code), int(createdby), str(created_on)
        ]
        q = "INSERT INTO tbl_units (client_id, business_group_id, legal_entity_id, division_id, category_id, " + \
            "country_id, geography_id, unit_code, unit_name, address, postal_code, created_by, created_on) values " + \
            " (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        unit_id = self._source_db.execute_insert(
            q, insert_value
        )
        if unit_id is False:
            raise process_error("E056")
        return unit_id

    def save_units_domain_organizations(self, unit_id, domain_orgn_ids):
        columns = ["unit_id", "domain_id", "organisation_id"]
        values = []
        for d_o in domain_orgn_ids :
            domain_id = d_o.split("-")[0].strip()
            org_id = d_o.split("-")[1].strip()
            values.append((unit_id, int(domain_id), int(org_id)))
        if values :
            self._source_db.bulk_insert("tbl_units_organizations", columns, values)

    def save_executive_message(self, csv_name, groupname, createdby):
        # Message for Compfie admin
        text = "Client Unit file %s of %s uploaded for  your approval" % (
                csv_name, groupname,
            )
        link = "/knowledge/approve_client_unit_bu"
        save_messages(self._source_db, 1, "Client Unit Bulk Upload", text, link, createdby)

        action = "Client Unit csv file uploaded %s of %s " % (
            csv_name, groupname
        )
        self._source_db.save_activity(createdby, frmClientUnitBulkUpload, action)

        # Message for techno manager
        text = "Client Unit file %s of %s uploaded for  your approval" % (
                csv_name, groupname,
            )
        link = "/knowledge/approve_client_unit_bu"
        save_messages(self._source_db, 5, "Client Unit Bulk Upload", text, link, createdby)

        action = "Client Unit csv file uploaded %s of %s " % (
            csv_name, groupname
        )
        self._source_db.save_activity(createdby, frmClientUnitBulkUpload, action)

    def save_manager_message(self, a_type, csv_name, groupname, createdby):
        if a_type == 1 :
            action_type = "approved"
        else :
            action_type = "rejected"
        # Message for Compfie admin
        text = "Client Unit file %s of %s has been %s" % (
                csv_name, groupname, action_type
            )
        link = "/knowledge/client-unit-bu"
        save_messages(self._source_db, 1, "Approve Client Unit Bulk Upload", text, link, createdby)

        action = "Client Unit file  %s of %s has been %s" % (
            csv_name, groupname, action_type
        )
        self._source_db.save_activity(createdby, frmApproveClientUnitBulkUpload, action)

        # Message for techno executive
        text = "Client Unit file %s of %s has been %s" % (
                csv_name, groupname, action_type
            )
        link = "/knowledge/client-unit-bu"
        save_messages(self._source_db, 6, "Approve Client Unit Bulk Upload", text, link, createdby)

        action = "Client Unit file  %s of %s has been %s" % (
            csv_name, groupname, action_type
        )
        self._source_db.save_activity(createdby, frmApproveClientUnitBulkUpload, action)


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

        self._temp_client_units = {}
        self._temp_units_count = {}
        self._legal_entity_name = None
        self._valid_unit_count = 0
        self._doc_names = []
        self._sheet_name = "Client Unit"

    def errorSummary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error" : 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0,
            "max_unit_count_error": 0
        }

    def compare_csv_columns(self):
        res = collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)
        if res is False :
            raise ValueError("Csv Column Mismatched")

    def check_duplicate_in_csv(self):
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Csv data Duplicate Found")

    def check_duplicate_unit_code_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"], x["Unit_Code"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1 :
                msg.append(grouped_list[0].get("Unit_Code"))

        if len(msg) > 0 :
            error_msg = "Duplicate unit code found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    def get_tempDB_data(self):
        # To get the unit codes under legal entity
        res = self._db.call_proc("sp_groups_client_units_list", [self._client_id])
        for d in res:
            self._temp_client_units[d["legal_entity"] + "-" + d["unit_code"]] = d

        # To get the domains, organization and its count under legal entity
        res = self._db.call_proc("sp_get_domain_organization_count", [self._client_id])
        for d in res:
            self._temp_units_count[d["legal_entity"] + "-" + d["organization"]] = d

    def check_duplicate_unit_code_in_tempDB(self, unit_code):
        tempStore = self._temp_client_units
        data = tempStore.get(self._legal_entity_name + "-" + unit_code)
        errDesc = []

        if data is not None:
            errDesc.append(unit_code + " duplication " + "in TempDB ")
        return errDesc

    def check_organization_unit_count_in_tempDB(self, organization_name):
        mainStrore = self.Organization
        tempStore = self._temp_units_count
        tempData = tempStore.get(self._legal_entity_name + "-" + organization_name.strip())
        errDesc = []
        if organization_name.find(CSV_DELIMITER) > 0:
            splittedOrg = organization_name.split(CSV_DELIMITER)
            for d in splittedOrg:
                mainData = mainStrore.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if mainData is not None and tempData is not None:
                    main_temp_units = int(mainData.get("total_unit_count")) - (int(mainData.get("created_units")) + int(tempData.get("saved_units")))
                    if main_temp_units == 0:
                        if errDesc is not None:
                            errDesc.append(d + " Unit count reached the limit")
                        else:
                            errDesc.extend(d + " Unit count reached the limit")
                    else:
                        if self._valid_unit_count > main_temp_units:
                            if errDesc is not None:
                                errDesc.append(d + " Unit count reached the limit")
                            else:
                                errDesc.extend(d + " Unit count reached the limit")
                        else:
                            self._valid_unit_count += 1
        else:
            mainData = mainStrore.get(str(self.Legal_Entity_Id) + "-" + organization_name)
            tempData = tempStore.get(self._legal_entity_name + "-" + organization_name)
            if mainData is not None and tempData is not None:
                main_temp_units = int(mainData.get("total_unit_count")) - (int(mainData.get("created_units")) + int(tempData.get("saved_units")))
                if main_temp_units == 0:
                    errDesc.append(organization_name + " Unit count reached the limit")
                else:
                    if self._valid_unit_count > main_temp_units:
                        errDesc.append(organization_name + " Unit count reached the limit")
                    else:
                        self._valid_unit_count += 1
        return errDesc

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
        self.check_duplicate_in_csv()
        self.check_duplicate_unit_code_in_csv()
        self.get_tempDB_data()
        self.init_values(self._session_user_obj.user_id(), self._client_id)

        for row_idx, data in enumerate(self._source_data):

            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)
                res = True
                unitCodeRes = True
                unitCodeErr = None
                unitCountErr = None
                unitCountRes = True
                error_count = {
                    "mandatory": 0,
                    "max_length": 0,
                    "invalid_char": 0
                }
                if (key == "Format" and value != ''):
                    self._doc_names.append(value)
                for v in values :
                    v = v.strip()
                    if key == "Legal_Entity":
                        self._legal_entity_name = v
                    elif key == "Unit_Code" and v != "auto_gen":
                        unitCodeErr = self.check_duplicate_unit_code_in_tempDB(v)
                        if len(unitCodeErr) > 0:
                            unitCodeRes = False
                            self._error_summary["duplicate_error"] += 1
                    elif key == "Organization":
                        unitCountErr = self.check_organization_unit_count_in_tempDB(value)
                        if len(unitCountErr) > 0:
                            unitCountRes = False

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
                                if key != "Division" and key != "Category" and key != "Unit_Code":
                                    self._error_summary["invalid_data_error"] += 1

                if (res is not True or unitCountRes is not True or unitCodeRes is not True) and key != "Division" and key != "Category":
                    # mapped_error_dict[row_idx] = CSV_DELIMITER.join(res)
                    error_list = mapped_error_dict.get(row_idx)

                    if error_list is None:
                        if unitCodeErr is not None:
                            error_list = unitCodeErr
                        elif unitCountErr is not None:
                            error_list = unitCountErr
                        else:
                            if key != "Unit_Code":
                                error_list = res
                    else :
                        if unitCodeErr is not None:
                            error_list.extend(unitCodeErr)
                        elif unitCountErr is not None:
                            error_list.extend(unitCountErr)
                        else:
                            if key != "Unit_Code":
                                error_list.extend(res)

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
                    self._error_summary["max_unit_count_error"] += 1
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
            "max_unit_count_error": self._error_summary["max_unit_count_error"],
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

class ValidateClientUnitsBulkDataForApprove(SourceDB):
    def __init__(self, db, csv_id, client_id, session_user):
        SourceDB.__init__(self)
        self._db = db
        self._csv_id = csv_id
        self._client_id = client_id
        self._session_user_obj = session_user
        self._temp_data = None
        self._declined_row_idx = []
        self.get_uploaded_data()
        self._group_name = None
        self._csv_name = None

    def get_uploaded_data(self):
        self._temp_data = self._db.call_proc("sp_bulk_client_unit_by_csvid", [self._csv_id])

    def check_for_system_declination_errors(self):
        sys_declined_count = 0
        self._declined_bulk_unit_id = []
        self.init_values(self._session_user_obj.user_id(), self._client_id)

        for row_idx, data in enumerate(self._temp_data):
            if row_idx == 0 :
                self._group_name = data.get("client_group")
                self._csv_name = data.get("csv_name")

            for key in self._csv_column_name:
                value = data.get(key)
                if key == "Postal_Code":
                    value = str(value)
                isFound = ""
                if value is None :
                    continue

                values = value.strip().split(CSV_DELIMITER)
                csvParam = csv_params.get(key)
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
                            if key != "Division" and key != "Category" and key != "Unit_Code":
                                sys_declined_count += 1

            if sys_declined_count > 0 :
                self._declined_bulk_unit_id.append(data.get("bulk_unit_id"))
        return self._declined_bulk_unit_id

    def process_data_to_main_db_insert(self):
        self._temp_data.sort(key=lambda x: (
             x["Legal_Entity"], x["Division"], x["Category"]
        ))
        for k, v in groupby(self._temp_data, key=lambda s: (
            s["Legal_Entity"], s["Division"], s["Category"]
        )):
            grouped_list = list(v)
            if len(grouped_list) == 0:
                continue
            value = grouped_list[0]
            le_id = None
            cl_id = self._client_id
            grp_name = value.get("client_group")
            bg_id = self.Business_Group_Id
            c_id = self.Country_Id
            created_by = value.get("uploaded_by")
            main_division_id = None
            main_category_id = None
            main_geo_id = None
            unit_code = None
            unit_name = value.get("Unit_Name")
            unit_address = value.get("Unit_Address") + "," + value.get("City") + "," + value.get("State")
            post_code = value.get("Postal_Code")
            domain_orgn_ids = []
            # orgn_ids = []

            # fetch legal_entity_id
            le_id = self.Legal_Entity.get(value.get("Legal_Entity")).get("legal_entity_id")

            # fetch division id
            division = value.get("Division")
            if self.Division.get(division) is None:
                main_division_id = self.save_division(cl_id, le_id, bg_id, division, created_by)
            else:
                main_division_id = self.Division.get(division).get("division_id")

            # fetch division id
            category = value.get("Category")
            if self.Category.get(category) is None:
                main_category_id = self.save_category(cl_id, le_id, bg_id, main_division_id, category, created_by)
            else:
                main_category_id = self.Category.get(category).get("category_id")

            geo_level_id = self.Geography_Level.get(str(c_id)+"-"+value.get("Geography_Level")).get("level_id")
            ul = value.get("Unit_Location")
            if geo_level_id == self.Unit_Location.get(ul).get("level_id"):
                main_geo_id = self.Unit_Location.get(ul).get("geography_id")

            if value.get("Unit_Code") == "auto_gen":
                unit_code = self.generate_unit_code(cl_id, grp_name)
            else:
                unit_code = str(value.get("Unit_Code")).strip()

            if value.get("Organization").find(CSV_DELIMITER) > 0:
                for orgn in value.get("Organization").strip().split(CSV_DELIMITER):
                    split_org = orgn.split(">>")
                    domain_orgn_ids.append(str(self.Domain.get(str(le_id)+"-"+split_org[0].strip()).get("domain_id"))+"-"+str(self.Organization.get(str(le_id)+"-"+orgn.strip()).get("organisation_id")))
            else:
                domain = value.get("Domain").strip()
                orgn = value.get("Organization").strip()
                split_org = orgn.split(">>")
                if domain == split_org[0].strip():
                    domain_orgn_ids.append(str(self.Domain.get(str(le_id) + "-" + domain).get("domain_id")) + "-" + str(self.Organization.get(str(le_id)+"-"+orgn).get("organisation_id")))

            unit_id = self.save_units(cl_id, bg_id, le_id, main_division_id, main_category_id, c_id, main_geo_id, unit_code, unit_name, unit_address, post_code, created_by)

            self.save_units_domain_organizations(unit_id, domain_orgn_ids)

    def make_rejection(self, declined_ids):
        q = "update tbl_bulk_units set action = 3 where bulk_unit_id in %s"
        self._source_db.execute_insert(q, [",".join(declined_ids)])
