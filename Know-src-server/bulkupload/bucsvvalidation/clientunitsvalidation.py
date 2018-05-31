import os
import collections
import traceback
import mysql.connector
import xlsxwriter
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME
)

from bulkupload.bulkconstants import (
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH, CSV_MAX_LINES
)

from server.common import (
    get_date_time
)
from server.database.forms import (
    frmClientUnitBulkUpload, frmApproveClientUnitBulkUpload
)
from server.exceptionmessage import process_error
from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    rename_file_type
)

__all__ = [
    "ValidateClientUnitsBulkCsvData",
    "ValidateClientUnitsBulkDataForApprove"
]
###########################################################################
'''
    SourceDB: This class methods executed with main db connection
    also check csv data validation
'''
##########################################################################


class SourceDB(object):

    def __init__(self):

        self._source_db = None
        self._source_db_con = None
        self._country = {}
        self._legal_entity = {}
        self._division = {}
        self._category = {}
        self._geography_level = {}
        self._unit_location = {}
        self._unit_code = {}
        self._domain = {}
        self._organization = {}
        self._legal_entity_id = None
        self._business_group_id = None
        self._country_id = None
        self._level_id = None
        self._csv_column_name = []
        self._main_domain_org = []
        self._csv_column_fields()
        self._auto_unit_code = None
        self._validation_method_maps = {}
        self._status_check_methods()
        self._connect_source_db()

    ###########################################################################
    '''
        csv_column_fields: This class methods contains the declaration of csv
        column names matched with the csv file
    '''
    ##########################################################################

    def _csv_column_fields(self):

        self._csv_column_name = [
            "Country", "Legal_Entity", "Division", "Category",
            "Geography_Level", "Unit_Location", "Unit_Code", "Unit_Name",
            "Unit_Address", "City", "State", "Postal_Code", "Domain",
            "Organization"
        ]

    ###########################################################################
    '''
        connect_source_db: This class methods connects to the main compfie
        knowledge database.
    '''
    ##########################################################################

    def _connect_source_db(self):

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

    ###########################################################################
    '''
        close_source_db: This class methods closes the main compfie
        knowledge database.
    '''
    ##########################################################################

    def close_source_db(self):

        self._source_db.close()
        self._source_db_con.close()

    ###########################################################################
    '''
        init_values: This class methods contains user id and client id as
        parameter to fetch the master db data for validation
    '''
    ##########################################################################

    def init_values(self, user_id, client_id):

        self.get_countries(user_id)
        self.get_legal_entities(user_id, client_id)
        self.get_divisions(client_id)
        self.get_categories(client_id)
        self.get_geography_level(user_id)
        self.get_unit_location()
        self.get_unit_code(client_id)
        self.get_domains_organizations(client_id)

    ###########################################################################
    '''
        get_countries: This class methods contains user id
        as parameter to fetch the master db countries list under a user
    '''
    ##########################################################################

    def get_countries(self, user_id):

        data = self._source_db.call_proc("sp_bu_countries", [user_id])
        for d in data:
            self._country[d["country_name"]] = d

    ###########################################################################
    '''
        get_legal_entities: This class methods contains user id and client id
        as parameter to fetch the master db legal entities under a client user
    '''
    ##########################################################################

    def get_legal_entities(self, user_id, client_id):

        data = self._source_db.call_proc_with_multiresult_set(
            "sp_bu_legal_entities", [client_id, user_id], 2
        )
        for d in data[1]:
            self._legal_entity[
                str(d["country_id"]) + "-" + d["legal_entity_name"]] = d

    ###########################################################################
    '''
        get_divisions: This class methods contains client id as
        parameter to fetch the master db division under a client
    '''
    ##########################################################################

    def get_divisions(self, client_id):

        data = self._source_db.call_proc("sp_bu_divisions", [client_id])
        for d in data:
            self._division[
                str(d["legal_entity_id"]) + "-" + d["division_name"]
            ] = d

    ###########################################################################
    '''
        get_categories: This class methods contains client id as
        parameter to fetch the master db categories under a client
    '''
    ##########################################################################

    def get_categories(self, client_id):

        data = self._source_db.call_proc("sp_bu_categories", [client_id])
        for d in data:
            self._category[
                str(d["legal_entity_id"]) + "-" + d["category_name"]
            ] = d

    ###########################################################################
    '''
        get_geography_level: This class methods contains user id as
        parameter to fetch the master db geography levels under a user
    '''
    ##########################################################################

    def get_geography_level(self, user_id):

        data = self._source_db.call_proc("sp_bu_geography_levels", [user_id])
        for d in data:
            self._geography_level[
                str(d["country_id"]) + '-' + d["level_name"]
            ] = d

    ###########################################################################
    '''
        get_unit_location: This class methods used to fetch the master db
        unit location under a level id
    '''
    ##########################################################################

    def get_unit_location(self):

        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data:
            newUnitLocation = ''
            for parentname in d["parent_names"].split('>>'):
                newUnitLocation = newUnitLocation + parentname.strip() + '>>'
            newUnitLocation = newUnitLocation[:-2]
            self._unit_location[newUnitLocation] = d

    ###########################################################################
    '''
        get_unit_code: This class methods contains client id as a parameter
        used to fetch the master db unit code under aa client
    '''
    ##########################################################################

    def get_unit_code(self, client_id):

        data = self._source_db.call_proc("sp_bu_unit_code", [client_id])
        for d in data:
            self._unit_code[d["unit_code"]] = d

    ###########################################################################
    '''
        get_domains_organizations: This class methods contains client id as a
        parameter used to fetch the master db domain and organization under a
        client id
    '''
    ##########################################################################

    def get_domains_organizations(self, client_id):

        data = self._source_db.call_proc(
            "sp_bu_domains_organization_unit_count",
            [client_id]
        )
        for d in data:
            self._domain[
                str(d["legal_entity_id"]) + "-" + d["domain_name"]
            ] = d
            self._organization[
                str(d["legal_entity_id"]) +
                "-" + d["domain_name"] +
                ">>" + d["organization_name"]
            ] = d

    ##############################################################
    '''
        check_base: This class methods contains status check value,
        list of the key, key value, field name to check whether
        the record is active/ inactive

    '''
    ###############################################################

    def check_base(self, check_status, store, key_name, status_name):
        data = store.get(key_name)
        if (data is not None and check_status is True):
            if status_name is None:
                if data.get("is_active") == 0:
                    return "Status Inactive"
            elif status_name == "domain_is_active":
                if data.get("domain_is_active") == 0:
                    if key_name.find("-") != -1:
                        return key_name.split("-")[1] + " Status Inactive"
                    else:
                        return key_name + " Status Inactive"
            elif status_name == "organization_is_active":
                if data.get("organization_is_active") == 0:
                    if key_name.find("-") != -1:
                        return key_name.split("-")[1] + " Status Inactive"
                    else:
                        return key_name + " Status Inactive"
        return True

    ###########################################################################
    '''
        check_country: This class methods contains country name
        to check whether the country is available for transaction

    '''
    ###########################################################################

    def check_country(self, country_name):
        store = self._country
        data = store.get(country_name)
        if data is not None:
            self._country_id = data.get("country_id")
            return self.check_base(False, store, country_name, None)
        else:
            return "Not found"

    ###########################################################################
    '''
        check_legal_entity: This class methods contains legal entity name
        to check whether the legal entity is available for transaction

    '''
    ###########################################################################

    def check_legal_entity(self, legal_entity_name):

        store = self._legal_entity
        data = store.get(str(self._country_id) + "-" + legal_entity_name)
        if (
            data is not None and
            data.get("is_closed") == 0 and
            data.get("is_approved") == 1 and
            data.get("le_contract_days") >= 0 and
            self._uploaded_by is not None and (
                self._uploaded_by == data.get("user_id")
            )
        ):
            self._legal_entity_id = data.get("legal_entity_id")
            self._business_group_id = data.get("business_group_id")
            return self.check_base(False, store, legal_entity_name, None)
        else:
            if data is None:
                return "Not found"
            elif data is not None and \
                (
                    data.get("is_closed") == 1 or
                    data.get("le_contract_days") < 0
                    ):
                return "Status Inactive"
            elif data is not None and data.get("is_approved") == 0:
                return "Not found"
            elif data is not None and (self._uploaded_by is not None and (
                self._uploaded_by != data.get("user_id"))
            ):
                return "Not assigned to the Techno Executive"

    ###########################################################################
    '''
        check_division: This class methods contains division name
        to check whether the division is available for transaction

    '''
    ###########################################################################

    def check_division(self, division_name):

        store = self._division
        data = store.get(str(self._legal_entity_id) + "-" + division_name)
        if data is not None:
            return self.check_base(False, self._division, division_name, None)
        else:
            return True

    ################################################################
    '''
        check_category: This class methods contains category name
        to check whether the category is available for transaction

    '''
    ################################################################

    def check_category(self, category_name):

        store = self._category
        data = store.get(str(self._legal_entity_id) + "-" + category_name)
        if data is not None:
            if (data.get("legal_entity_id") == self._legal_entity_id):
                return self.check_base(
                    False, self._category, category_name, None
                )
            else:
                return True
        else:
            return True

    #########################################################################
    '''
        check_geography_level: This class methods contains geography level
        name to check whether the geography level is available for
        transaction
    '''
    ##########################################################################

    def check_geography_level(self, level_name):

        store = self._geography_level
        data = store.get(str(self._country_id) + '-' + level_name)
        if data is not None:
            if (
                data.get("country_id") == self._country_id and
                data.get("level_name") == level_name
            ):
                self._level_id = data.get("level_id")
                return self.check_base(
                    True, self._geography_level,
                    (str(self._country_id) + '-' + level_name), None
                )
            else:
                return "Not found"
        else:
            return "Not found"

    #######################################################################
    '''
        check_unit_location: This class methods contains geography name
        to check whether the geography name is available for transaction

    '''
    #######################################################################

    def check_unit_location(self, geography_name):
        store = self._unit_location
        newGeoName = ''
        for geo in geography_name.split('>>'):
            newGeoName = newGeoName + geo.strip() + '>>'
        newGeoName = newGeoName[:-2]
        data = store.get(newGeoName)
        if data is not None:
            if (data.get("level_id") == self._level_id):
                return self.check_base(
                    True,
                    self._unit_location, newGeoName, None
                )
            else:
                return "Not found"
        else:
            return "Not found"

    ##################################################################
    '''
        check_unit_code: This class methods contains unit code
        to check whether the unit code is already created under the
        legal entity
    '''
    ##################################################################

    def check_unit_code(self, unit_code):
        if unit_code != "auto_gen" and unit_code.isalnum():
            store = self._unit_code
            data = store.get(unit_code)
            if data is not None:
                if (data.get("legal_entity_id") != self._legal_entity_id):
                    return self.check_base(
                        False, self._unit_code,
                        unit_code, None
                    )
                else:
                    return unit_code + \
                        " Duplication in Main DB"
            else:
                return True
        else:
            return True

    ##############################################################
    '''
        check_domain: This class methods contains domain name
        to check whether the domain is under the legal entity

    '''
    ##############################################################

    def check_domain(self, domain_name):
        store = self._domain
        errDesc = []
        status = None
        newDomainName = ''
        for domain in domain_name.split('|;|'):
            newDomainName = newDomainName + domain.strip() + '|;|'
        newDomainName = newDomainName[:-2]
        if domain_name.find(CSV_DELIMITER) > 0:
            splittedDomain = domain_name.split(CSV_DELIMITER)
            for d in splittedDomain:
                data = store.get(str(self._legal_entity_id) + "-" + d.strip())
                if data is not None:
                    status = self.check_base(
                        True, self._domain,
                        (str(self._legal_entity_id) + "-" + d.strip()),
                        "domain_is_active"
                    )
                    if status is "Status Inactive":
                        errDesc.append(d + status)
                else:
                    errDesc.append(d + " Not Found")
        else:
            data = store.get(
                str(self._legal_entity_id) + "-" + domain_name.strip()
            )
            if data is not None:
                return self.check_base(
                    True, self._domain,
                    (str(self._legal_entity_id) + "-" + domain_name.strip()),
                    "domain_is_active"
                )
            else:
                errDesc.append(domain_name + " Not Found")

        if len(errDesc) > 0:
            return ','.join(errDesc)

    #######################################################################
    '''
        check_organization_under_domain: This class method is defined
        to check the whether each domain has organization inside a csv row
    '''
    #######################################################################

    def check_organization_under_domain(self, domain_name, orgn_name):
        msg = []
        if domain_name.strip().find(CSV_DELIMITER) >= 0:
            splitDomain = domain_name.split(CSV_DELIMITER)
            for d in splitDomain:
                if orgn_name.find(d.strip()) < 0:
                    msg.append(
                        "Organization - " + d.strip() +
                        " organization is blank"
                    )
        else:
            if orgn_name.find(CSV_DELIMITER) >= 0:
                for o in orgn_name.split(CSV_DELIMITER):
                    if o.find(domain_name.strip()) < 0:
                        msg.append(
                            "Organization - " + o.strip() +
                            " invalid data"
                        )
            else:
                if orgn_name.find(domain_name.strip()) < 0:
                    msg.append(
                        "Organization - " + domain_name.strip() +
                        " organization is blank"
                    )
        if len(msg) > 0:
            return ','.join(msg)

    #######################################################################
    '''
        check_organization: This class methods contains organization name
        to check whether the organization is under the legal entity

    '''
    #######################################################################

    def check_organization(self, organization_name):
        store = self._organization
        errDesc = []
        status = None
        newOrgnName = ''
        for org in organization_name.split('>>'):
            newOrgnName = newOrgnName + org.strip() + '>>'
        newOrgnName = newOrgnName[:-2]
        if newOrgnName.find(CSV_DELIMITER) > 0:
            splittedOrg = newOrgnName.split(CSV_DELIMITER)
            for d in splittedOrg:
                data = store.get(str(self._legal_entity_id) + "-" + d.strip())
                if data is not None:
                    status = self.check_base(
                        True, self._organization,
                        (str(self._legal_entity_id) + "-" + d.strip()),
                        "organization_is_active"
                    )
                    if status is "Status Inactive":
                        errDesc.append(d.strip() + status)
                    else:
                        self.save_main_domain_orgn_units(
                            self._legal_entity_id, d.strip()
                        )
                        for dat in self._main_domain_org:
                            split_val = dat.split("-")
                            if(
                                split_val[0] ==
                                str(self._legal_entity_id) and
                                split_val[1] == d.strip()
                            ):
                                csv_units = int(split_val[2])
                                break

                        main_db_units = int(data.get("created_units")) +\
                            int(csv_units)
                        if (
                            int(main_db_units) >
                            int(data.get("total_unit_count"))
                        ):
                            errDesc.append(
                                d.strip() +
                                " Unit count exceeds the limit in Main DB"
                                )
                else:
                    errDesc.append(d.strip() + " Not Found")

        else:
            data = store.get(
                str(self._legal_entity_id) + "-" + newOrgnName.strip()
            )
            if data is not None:
                self.save_main_domain_orgn_units(
                    self._legal_entity_id, newOrgnName.strip()
                )
                for dat in self._main_domain_org:
                    split_val = dat.split("-")
                    if(
                        split_val[0] ==
                        str(self._legal_entity_id) and
                        split_val[1] == newOrgnName.strip()
                    ):
                        csv_units = int(split_val[2])
                        break

                main_db_units = int(data.get("created_units")) +\
                    int(csv_units)
                if (
                    int(main_db_units) >
                    int(data.get("total_unit_count"))
                ):
                    errDesc.append(
                        newOrgnName.strip() +
                        " Unit count exceeds the limit in Main DB"
                    )
                else:
                    return self.check_base(
                        True, self._organization,
                        (str(self._legal_entity_id) + "-" +
                            newOrgnName.strip()),
                        "organization_is_active")
            else:
                errDesc.append(newOrgnName.strip() + " Not Found")

        if len(errDesc) > 0:
            return ','.join(errDesc)

    def save_main_domain_orgn_units(self, le_id, domain_org):
        if len(self._main_domain_org) == 0:
            self._main_domain_org.append(
                str(le_id).strip() + "-" +
                domain_org.strip() + "-1"
            )
        else:
            # join_csv = ','.join(self._csv_domain_orgn)
            # self._csv_domain_orgn = []
            occur = 0
            for i, data in enumerate(self._main_domain_org):
                split_val = data.split("-")
                if(
                    split_val[0] == str(le_id).strip() and
                    split_val[1] == domain_org.strip()
                ):
                    occur += 1
                    save_unit = int(
                        split_val[2].strip()) + 1
                    self._main_domain_org.pop(i)
                    self._main_domain_org.append(
                        str(le_id).strip() +
                        "-" +
                        domain_org.strip() + "-" + str(save_unit)
                    )
                    break
            if occur == 0:
                self._main_domain_org.append(
                    str(le_id).strip() +
                    "-" +
                    domain_org.strip() + "-" + "1")

    def _status_check_methods(self):
        self._validation_method_maps = {
            "Country": self.check_country,
            "Legal_Entity": self.check_legal_entity,
            "Division": self.check_division,
            "Category": self.check_category,
            "Geography_Level": self.check_geography_level,
            "Unit_Location": self.check_unit_location,
            "Unit_Code": self.check_unit_code,
            "Domain": self.check_domain,
            "Organization": self.check_organization
        }

    ###################################################################
    '''
        save_division: This class methods is defined to store the
        division under client in master DB
    '''
    ###################################################################

    def save_division(self, cl_id, le_id, bg_id, division_name, createdby):

        created_on = get_date_time()
        if bg_id is not None:
            bg_id = int(bg_id)
        else:
            bg_id = None
        insert_value = [
            int(cl_id), int(le_id),
            bg_id, division_name,
            int(createdby), str(created_on)
        ]
        q = "INSERT INTO tbl_divisions (client_id, legal_entity_id, "\
            " business_group_id, division_name, created_by, " + \
            "created_on) values " + \
            " (%s, %s, %s, %s, %s, %s)"
        division_id = self._source_db.execute_insert(
            q, insert_value
        )
        if division_id is False:
            raise process_error("E054")
        return division_id

    ####################################################################
    '''
        save_category: This class methods is defined to store the
        category under client in master DB
    '''
    #####################################################################

    def save_category(
        self, cl_id, le_id, bg_id, division_id, category_name, createdby
    ):

        created_on = get_date_time()
        if bg_id is not None:
            bg_id = int(bg_id)
        else:
            bg_id = None
        insert_value = [
            int(cl_id), int(le_id),
            bg_id, int(division_id),
            category_name, int(createdby), str(created_on)
        ]
        q = "INSERT INTO tbl_categories ( " + \
            "client_id, legal_entity_id, business_group_id, " + \
            "division_id, category_name, created_by, created_on) values " + \
            " (%s, %s, %s, %s, %s, %s, %s)"
        category_id = self._source_db.execute_insert(
            q, insert_value
        )
        if category_id is False:
            raise process_error("E093")
        return category_id

    ###################################################################
    '''
        generate_unit_code: This class methods is defined to
        generate unit code in master DB
    '''
    ###################################################################

    def generate_unit_code(self, cl_id, grp_name, le_id, u_code):

        if u_code is None:
            unit_code_start_letters = grp_name[:2].upper()
            select_param = [
                str(unit_code_start_letters),
                str(unit_code_start_letters),
                int(cl_id), int(le_id)
            ]
            unit_code = None
            q = "SELECT (max(TRIM(LEADING %s FROM unit_code))+1) as code " + \
                "FROM tbl_units WHERE unit_code like binary " + \
                "concat( %s,'%') and " + \
                "CHAR_LENGTH(unit_code) = 7 and client_id=%s and " + \
                "legal_entity_id = %s; "
            uc = self._source_db.select_one(
                q, select_param
            )
            if uc["code"] is not None:
                u_code = int(uc["code"])
            else:
                u_code = 1

            if uc is False:
                raise process_error("E056")
            else:
                if (u_code > 0 and u_code < 10):
                    unit_code = str(
                        unit_code_start_letters
                    ) + '0000' + str(u_code)
                elif (u_code >= 10 and u_code < 100):
                    unit_code = str(
                        unit_code_start_letters
                    ) + '000' + str(u_code)
                elif (u_code >= 100 and u_code < 1000):
                    unit_code = str(
                        unit_code_start_letters
                    ) + '00' + str(u_code)
                elif (u_code >= 1000 and u_code < 10000):
                    unit_code = str(
                        unit_code_start_letters
                    ) + '0' + str(u_code)
        else:
            unit_code_start_letters = grp_name[:2].upper()
            if (u_code > 0 and u_code < 10):
                unit_code = str(unit_code_start_letters) + \
                    '0000' + str(u_code)
            elif (u_code >= 10 and u_code < 100):
                unit_code = str(unit_code_start_letters) + \
                    '000' + str(u_code)
            elif (u_code >= 100 and u_code < 1000):
                unit_code = str(unit_code_start_letters) + \
                    '00' + str(u_code)
            elif (u_code >= 1000 and u_code < 10000):
                unit_code = str(unit_code_start_letters) + \
                    '0' + str(u_code)
        return unit_code

    ##################################################################
    '''
        save_units: This class methods is defined to save the units
        in master DB
    '''
    ##################################################################

    # write update query

    def save_units(
        self, cl_id, bg_id, le_id, division_id, category_id, country_id,
        groupName, data, system_declined_units, createdby

    ):
        created_on = get_date_time()
        values, domain_orgn_ids, auto_gen_ids = [], [], []
        inserted_records = 0
        auto_gen_data = {}
        for idx, d in enumerate(data):
            if (
                (len(system_declined_units) == 0 or
                    (len(system_declined_units) > 0 and
                        d["bulk_unit_id"] not in system_declined_units)) and
                    (int(d["action"]) == 0 or int(d["action"]) == 1 or
                        int(d["action"]) == 2)
            ):
                if d["Unit_Code"] == "auto_gen":
                    auto_gen_ids.append(d["bulk_unit_id"])
                    auto_gen_data[d["bulk_unit_id"]] = d
                else:
                    unit_code = str(d["Unit_Code"]).strip()
                    if bg_id is not None:
                        bg_id = int(bg_id)
                    else:
                        bg_id = None
                    unit_name = d["Unit_Name"]
                    unit_address = d["Unit_Address"] + "," + \
                        d["City"] + "," + d["State"]
                    post_code = d["Postal_Code"]
                    main_geo_id = None
                    geo_level_id = self._geography_level.get(
                        str(country_id) + "-" + d["Geography_Level"]
                    ).get("level_id")
                    newul = ''
                    for ul in d["Unit_Location"].split('>>'):
                        newul = newul + ul.strip() + '>>'
                    newul = newul[:-2]
                    if geo_level_id == (
                        self._unit_location.get(newul).get("level_id")
                    ):
                        main_geo_id = self._unit_location. \
                            get(newul).get("geography_id")
                    if d["Organization"].find(CSV_DELIMITER) > 0:
                        for orgn in d["Organization"].strip(). \
                                split(CSV_DELIMITER):
                            split_org = orgn.split(">>")
                            neworgn = ''
                            for o in orgn.split('>>'):
                                neworgn = neworgn + o.strip() + '>>'
                            neworgn = neworgn[:-2]

                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self._domain.get(
                                        str(le_id) + "-" + split_org[0].strip()
                                    ).get("domain_id")) + "-" +
                                str(
                                    self._organization.get(
                                        str(le_id) + "-" + neworgn.strip()
                                    ).get("organisation_id")
                                ))
                    else:
                        domain = d["Domain"].strip()
                        orgn = d["Organization"].strip()
                        split_org = orgn.split(">>")
                        neworgn = ''
                        for o in orgn.split('>>'):
                            neworgn = neworgn + o.strip() + '>>'
                        neworgn = neworgn[:-2]
                        if domain == split_org[0].strip():
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(self._domain.get
                                    (
                                        str(le_id) + "-" + domain
                                    ).get("domain_id")) + "-" +
                                str(self._organization.get(
                                    str(le_id) + "-" + neworgn
                                ).get("organisation_id")))
                    if int(d["action"]) == 0 or int(d["action"]) == 1:
                        action_val = 1
                        remarks_text = None
                    else:
                        action_val = int(d["action"])
                        remarks_text = d["remarks"]
                    self._auto_unit_code = unit_code
                    values.append((
                        int(cl_id), bg_id, int(le_id), int(division_id),
                        int(category_id), int(country_id), int(main_geo_id),
                        str(unit_code), str(unit_name),
                        str(unit_address), str(post_code), action_val,
                        int(createdby), str(created_on), remarks_text,
                        int(createdby), str(created_on)
                    ))
                    inserted_records += 1
        if values:
            self.process_db_saving(
                values, inserted_records, cl_id, domain_orgn_ids, le_id
            )
        self.process_auto_gen_codes(
            auto_gen_ids, auto_gen_data, bg_id, cl_id, groupName, le_id,
            country_id, division_id, category_id, createdby
        )

    def process_auto_gen_codes(
        self, auto_gen_ids, auto_gen_data, bg_id, cl_id, groupName, le_id,
        country_id, division_id, category_id, createdby
    ):
        inserted_records = 0
        incre = 1
        values = []
        created_on = get_date_time()
        domain_orgn_ids = []
        if len(auto_gen_ids) > 0:
            for b_u_id in auto_gen_ids:
                unit_data = auto_gen_data.get(b_u_id)
                if unit_data is not None:
                    if bg_id is not None:
                        bg_id = int(bg_id)
                    else:
                        bg_id = None
                    unit_name = unit_data.get("Unit_Name")
                    unit_address = unit_data.get("Unit_Address") + "," + \
                        unit_data.get("City") + "," + unit_data.get("State")
                    post_code = unit_data.get("Postal_Code")
                    print "self._auto_unit_code"
                    print self._auto_unit_code
                    if self._auto_unit_code is None:
                        unit_code = self.generate_unit_code(
                            cl_id, groupName, le_id, None)
                    else:
                        u_code = int(self._auto_unit_code[2:]) + incre
                        unit_code = self.generate_unit_code(
                            cl_id, groupName, le_id, u_code)
                    main_geo_id = None
                    geo_level_id = self._geography_level.get(
                        str(country_id) + "-" + unit_data.get(
                            "Geography_Level")
                    ).get("level_id")
                    newul = ''
                    for ul in unit_data.get("Unit_Location").split('>>'):
                        newul = newul + ul.strip() + '>>'
                    newul = newul[:-2]
                    if geo_level_id == self._unit_location.\
                            get(newul).get("level_id"):
                        main_geo_id = self._unit_location.\
                            get(newul).get("geography_id")
                    if unit_data.get("Organization").find(CSV_DELIMITER) > 0:
                        for orgn in unit_data.get("Organization").\
                                strip().split(CSV_DELIMITER):
                            split_org = orgn.split(">>")
                            neworgn = ''
                            for o in orgn.split('>>'):
                                neworgn = neworgn + o.strip() + '>>'
                            neworgn = neworgn[:-2]

                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(self._domain.get(
                                        str(le_id) + "-" + split_org[0].strip()
                                    ).get("domain_id")) + "-" +
                                str(self._organization.get(
                                        str(le_id) + "-" + neworgn.strip()
                                    ).get("organisation_id"))
                            )
                    else:
                        domain = unit_data.get("Domain").strip()
                        orgn = unit_data.get("Organization").strip()
                        split_org = orgn.split(">>")
                        neworgn = ''
                        for o in orgn.split('>>'):
                            neworgn = neworgn + o.strip() + '>>'
                        neworgn = neworgn[:-2]
                        if domain == split_org[0].strip():
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self._domain.get(
                                        str(le_id) + "-" + domain
                                    ).get("domain_id")
                                ) + "-" +
                                str(
                                    self._organization.get(
                                        str(le_id) + "-" + neworgn
                                    ).get("organisation_id"))
                                )
                    if (
                        int(unit_data.get("action")) == 0 or
                        int(unit_data.get("action")) == 1
                    ):
                        action_val = 99
                        remarks_text = None
                    else:
                        action_val = int(unit_data.get("action"))
                        remarks_text = unit_data.get("remarks")
                    values.append((
                        int(cl_id), bg_id, int(le_id), int(division_id),
                        int(category_id), int(country_id), int(main_geo_id),
                        str(unit_code), str(unit_name),
                        str(unit_address), str(post_code), action_val,
                        int(createdby), str(created_on),
                        remarks_text, int(createdby), str(created_on)
                    ))
                    self._auto_unit_code = unit_code
                    inserted_records += 1
        if values:
            self.process_db_saving(
                values, inserted_records, cl_id, domain_orgn_ids, le_id
            )

    def process_db_saving(
        self, values, inserted_records, cl_id, domain_orgn_ids, le_id
    ):
        columns = [
            "client_id", "business_group_id", "legal_entity_id", "division_id",
            "category_id", "country_id", "geography_id", "unit_code",
            "unit_name", "address", "postal_code", "is_approved",
            "approved_by", "approved_on", "remarks", "created_by",
            "created_on"]

        self._source_db.bulk_insert("tbl_units", columns, values)
        last_id = str(self._auto_unit_code) + ";" + str(inserted_records)
        self.save_units_domain_organizations(
            last_id, cl_id, domain_orgn_ids, le_id
        )
        q = "update tbl_units set is_approved = %s where is_approved = %s"
        self._source_db.execute(q, [1, 99])

    ###################################################################
    '''
        save_units_domain_organizations: This class methods is
        defined to save the domains and organizations under a
        unit in master DB
    '''
    ###################################################################

    def save_units_domain_organizations(
        self, last_id, client_id, domain_orgn_ids, le_id
    ):
        splitLastID = last_id.split(";")
        q = "SELECT unit_id as max_id from tbl_units where unit_code = %s " + \
            "and legal_entity_id = %s; "
        u_id = self._source_db.select_one(
                q, [splitLastID[0].strip(), int(le_id)]
            )
        if int(splitLastID[1].strip()) < int(u_id["max_id"]):
            unit_start_id = int(u_id["max_id"]) - int(splitLastID[1].strip())
        else:
            unit_start_id = int(splitLastID[1].strip()) - int(u_id["max_id"])

        columns = ["unit_id", "domain_id", "organisation_id"]
        values = []
        unit_id = unit_start_id
        last = object()
        for d_o in domain_orgn_ids:
            u_code = d_o.split("-")[0].strip()
            if last != u_code:
                unit_id = unit_id + 1
                last = u_code
                domain_id = d_o.split("-")[1].strip()
                org_id = d_o.split("-")[2].strip()
                values.append((unit_id, int(domain_id), int(org_id)))
            else:
                domain_id = d_o.split("-")[1].strip()
                org_id = d_o.split("-")[2].strip()
                values.append((unit_id, int(domain_id), int(org_id)))
        if values:
            self._source_db.bulk_insert(
                "tbl_units_organizations", columns, values
            )

    ###################################################################
    '''
        save_executive_message: This class methods is defined to
        save the notification message to techno manager and compfie
        admin by techno executive
    '''
    ###################################################################

    def save_executive_message(self, full_csv_name, groupname, createdby):
        # Message for techno manager
        msg_user_id = []
        csv_name = full_csv_name.split('_')
        csv_name = "_".join(csv_name[:-1])

        text = "Client Unit File %s of %s uploaded for  your approval" % (
                csv_name, groupname,
            )
        link = "/knowledge/approve_client_unit_bu"

        q = "select t1.user_id from tbl_user_login_details as t1 " + \
            " inner join tbl_user_mapping as t2 on t2.parent_" + \
            "user_id = t1.user_id " + \
            " where t1.is_active = 1 and t2.child_user_id = %s "

        row = self._source_db.select_all(q, [createdby])

        for r in row:
            msg_user_id.append(r["user_id"])

        if msg_user_id is not None:
            self._source_db.save_toast_messages(
                5, "Client Unit Bulk Upload", text,
                link, msg_user_id, createdby
            )

        q1 = "select user_id from tbl_user_login_details where " + \
            "is_active = 1 and user_category_id = 1"

        row1 = self._source_db.select_all(q1)
        c_admin = []
        for r in row1:
            c_admin.append(r["user_id"])

        if len(c_admin) > 0:
            self._source_db.save_toast_messages(
                1, "Client Unit Bulk Upload", text, link, c_admin, createdby
            )

        action = "Client Unit csv file uploaded %s of %s " % (
            csv_name, groupname
        )
        self._source_db.save_activity(
            createdby, frmClientUnitBulkUpload, action
        )

    #####################################################################
    '''
        save_manager_message: This class methods is defined to save the
        notification message to techno executive and compfie admin
        by techno manager
    '''
    #####################################################################

    def save_manager_message(
        self, a_type, full_csv_name, groupname, createdby,
        uploaded_by, reject_reason, sys_decl_cnt
    ):
        if a_type == 1:
            action_type = "approved"
        else:
            action_type = "rejected"

        csv_name = full_csv_name.split('_')
        csv_name = "_".join(csv_name[:-1])

        # Message for techno executive
        msg_user_id = []
        if a_type == 1:
            text = "Client Unit File %s of %s has been %s" % \
                (csv_name, groupname, action_type)

            if sys_decl_cnt > 0:
                sysDeclText = "Client Unit File %s - %s - %s Unit(s) has "\
                    "been declined by COMPFIE" % \
                    (csv_name, groupname, sys_decl_cnt)
            # print sysDeclText
        else:
            text = "Client Unit File %s of %s has been %s with %s" % (
                    csv_name, groupname, action_type, reject_reason
                )
        link = "/knowledge/client-unit-bu"
        msg_user_id.append(uploaded_by)
        self._source_db.save_toast_messages(
            6, "Approve Client Unit Bulk Upload", text,
            link, msg_user_id, createdby
        )

        if sys_decl_cnt > 0:
            self._source_db.save_toast_messages(
                6, "Approve Client Unit Bulk Upload", sysDeclText,
                link, msg_user_id, createdby
            )
        q1 = "select user_id from tbl_user_login_details "\
            "where is_active = 1 and user_category_id = 1"
        row1 = self._source_db.select_all(q1)
        c_admin = []
        for r in row1:
            c_admin.append(r["user_id"])

        if len(c_admin) > 0:
            self._source_db.save_toast_messages(
                1, "Approve Client Unit Bulk Upload", text,
                link, c_admin, createdby
            )
            if sys_decl_cnt > 0:
                self._source_db.save_toast_messages(
                    1, "Approve Client Unit Bulk Upload",
                    sysDeclText, link, c_admin, createdby
                )

        action = "Client Unit file  %s of %s has been %s" % (
            csv_name, groupname, action_type
        )
        self._source_db.save_activity(
            createdby, frmApproveClientUnitBulkUpload, action
        )

    ###################################################################
    '''
        source_commit: This class methods is defined to commit the
        transaction made in master database
    '''
    ###################################################################

    def source_commit(self):
        self._source_db.commit()

######################################################################
'''
    ValidateClientUnitsBulkCsvData: This class is defined to validate
    the client unit bulk csv data for any system declination error
'''
######################################################################


class ValidateClientUnitsBulkCsvData(SourceDB):
    def __init__(
        self, db, source_data, session_user, client_id, csv_name, csv_header
    ):
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._client_id = client_id
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._error_summary = {}
        self.errorSummary()
        self._uploaded_by = None
        self._temp_client_units = {}
        self._temp_units_count = {}
        self._csv_domain_orgn = []
        self._legal_entity_name = None
        self._valid_unit_count = 1
        self._doc_names = []
        self._sheet_name = "Client Unit"

    #################################################################
    '''
        errorSummary: This class method is defined to store errors
        as per the category of the error
    '''
    #################################################################

    def errorSummary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error": 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0,
            "max_unit_count_error": 0
        }

    ##################################################################
    '''
        compare_csv_columns: This class method is defined to compare
        the csv coulmns header names with the self defined headers
    '''
    ##################################################################

    def compare_csv_columns(self):
        res = collections.Counter(self._csv_column_name) == \
            collections.Counter(self._csv_header)
        if res is False:
            # raise ValueError("Csv Column Mismatched")
            return "Csv Column Mismatched"

    ###################################################################
    '''
        check_duplicate_in_csv: This class method is defined to check
        duplicate values inside csv data
    '''
    ###################################################################

    def check_duplicate_in_csv(self):
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Csv data Duplicate Found")

    ###################################################################
    '''
        check_duplicate_unit_code_in_csv: This class method is defined
        to check the duplication of unit code in csv data
    '''
    ####################################################################

    def check_valid_unit_code_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"], x["Unit_Code"]
        ))
        unit_codes = []
        unit_code_invalid = 0
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if (
                grouped_list[0].get("Unit_Code") != '' and
                grouped_list[0].get("Unit_Code") is not None
            ):
                if grouped_list[0].get("Unit_Code").find("_") < 0:
                    if not grouped_list[0].get("Unit_Code").isalnum():
                        if len(grouped_list) >= 1:
                            unit_code_invalid += len(grouped_list)
                            unit_codes.append(grouped_list[0].get("Unit_Code"))
                    else:
                        letter_cnt = 0
                        num_cnt = 0
                        for i in grouped_list[0].get("Unit_Code"):
                            if i.isalpha():
                                letter_cnt += 1
                            if i.isdigit():
                                num_cnt += 1
                        if letter_cnt == 0 or num_cnt == 0:
                            unit_code_invalid += len(grouped_list)
                            unit_codes.append(grouped_list[0].get("Unit_Code"))
                else:
                    up_cnt = 0
                    if not grouped_list[0].get("Unit_Code").isalnum():
                        for i in grouped_list[0].get("Unit_Code"):
                            if i.isupper():
                                up_cnt += 1
                        if up_cnt > 0:
                            if len(grouped_list) >= 1:
                                unit_code_invalid += len(grouped_list)
                                unit_codes.append(
                                    grouped_list[0].get("Unit_Code")
                                )
                        else:
                            if grouped_list[0].get("Unit_Code") != "auto_gen":
                                if len(grouped_list) >= 1:
                                    unit_code_invalid += len(grouped_list)
                                    unit_codes.append(
                                        grouped_list[0].get("Unit_Code"))
                    else:
                        if len(grouped_list) >= 1:
                            unit_code_invalid += len(grouped_list)
                            unit_codes.append(grouped_list[0].get("Unit_Code"))
        return unit_code_invalid, unit_codes

    def check_duplicate_unit_code_in_csv(self):
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"], x["Unit_Code"]
        ))
        unit_codes = []
        unit_code_occur = 0
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1 and \
                    grouped_list[0].get("Unit_Code") != "auto_gen":
                unit_code_occur += len(grouped_list)
                unit_codes.append(grouped_list[0].get("Unit_Code"))

        return unit_code_occur, unit_codes

    ##################################################################
    '''
        check_duplicate_domain_in_csv_row: This class method is
        defined to check the duplication of domain in a csv row
    '''
    ##################################################################

    def check_duplicate_domain_in_csv_row(self):
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"], x["Domain"]
        ))
        domain_duplicates = []
        occur = 0
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Domain"]
        )):
            grouped_list = list(v)
            if grouped_list[0].get("Domain").find('|;|') >= 0:
                splitDomain = grouped_list[0].get("Domain").split('|;|')
                last = object()
                for val in splitDomain:
                    if last != val.strip():
                        last = val.strip()
                    else:
                        occur += 1
            if occur > 0:
                domain_duplicates.append(grouped_list[0].get("Domain"))
        return domain_duplicates

    ###################################################################
    '''
        check_duplicate_organization_in_csv_row: This class method is
        defined to check the duplication of organization inside a csv
        row
    '''
    ###################################################################

    def check_duplicate_organization_in_csv_row(self):
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"], x["Organization"]
        ))
        orgn_duplicates = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Organization"]
        )):
            grouped_list = list(v)
            occur = 0
            if grouped_list[0].get("Organization").find('|;|') >= 0:
                splitOrgn = grouped_list[0].get("Organization").split('|;|')
                last = object()
                for val in splitOrgn:
                    if last != val.strip():
                        last = val.strip()
                    else:
                        occur += 1
            if occur > 0:
                orgn_duplicates.append(grouped_list[0].get("Organization"))

        return orgn_duplicates

    #################################################################
    '''
        get_tempDB_data: This class method is defined to fetch the
        temp db data stored under a group/ legal entity and the
        domain/ organization created under the legal entity
    '''
    #################################################################

    def get_tempDB_data(self):

        # To get the unit codes under legal entity
        res = self._db.call_proc(
            "sp_groups_client_units_list", [self._client_id]
        )
        for d in res:
            self._temp_client_units[
                d["legal_entity"] + "-" + d["unit_code"]
            ] = d

        # To get the domains, organization and its count under legal entity
        res = self._db.call_proc(
            "sp_get_domain_organization_count", [self._client_id]
        )
        for d in res:
            neworgn = ''
            for o in d["organization"].split('>>'):
                neworgn = neworgn + o.strip() + '>>'
            neworgn = neworgn[:-2]
            self._temp_units_count[
                d["legal_entity"] + "-" + neworgn
            ] = d

    #################################################################
    '''
        check_duplicate_unit_code_in_tempDB: This class method is
        defined to check the unit code duplication in temp db
    '''
    #################################################################

    def check_duplicate_unit_code_in_tempDB(self, unit_code):
        tempStore = self._temp_client_units
        data = tempStore.get(self._legal_entity_name + "-" + unit_code)
        if data is not None:
            return "Unit_Code - " + unit_code + " duplication " + "in TempDB "

    ###################################################################
    '''
        check_organization_unit_count_in_tempDB: This class method is
        defined to check the organization's unit count under a legal
        entity
    '''
    ###################################################################

    def check_organization_unit_count_in_tempDB(self, organization_name):
        mainStrore = self._organization
        tempStore = self._temp_units_count
        saved_units, csv_units = 0, 0
        neworgn = ''
        for o in organization_name.split('>>'):
            neworgn = neworgn + o.strip() + '>>'
        neworgn = neworgn[:-2]
        tempData = tempStore.get(
            self._legal_entity_name + "-" + neworgn.strip()
        )
        errDesc = []
        if neworgn.find(CSV_DELIMITER) > 0:
            splittedOrg = neworgn.split(CSV_DELIMITER)
            for d in splittedOrg:
                saved_units = 0
                mainData = mainStrore.get(
                    str(self._legal_entity_id) + "-" + d.strip()
                )
                if mainData is not None:
                    for temp_d in tempStore:
                        if (
                            temp_d.split('-')[0].strip() ==
                            self._legal_entity_name.strip()
                        ):
                            tempData = tempStore.get(temp_d)
                            orgn_name = tempData.get("organization")
                            temporgn = ''
                            for o in orgn_name.split('>>'):
                                temporgn = temporgn + o.strip() + '>>'
                            temporgn = temporgn[:-2]
                            if d.strip() in temporgn.strip():
                                saved_units = saved_units +\
                                    int(tempData.get("saved_units"))
                    self.save_csv_domain_orgn_units(
                            self._legal_entity_name, d)
                    for data in self._csv_domain_orgn:
                        split_val = data.split("-")
                        if(
                            split_val[0] ==
                            self._legal_entity_name.strip() and
                            split_val[1] == d.strip()
                        ):
                            csv_units = int(split_val[2])
                            break
                    main_temp_units = int(mainData.get("created_units")) +\
                        int(saved_units) + int(csv_units)
                    if main_temp_units > mainData.get("total_unit_count"):
                        errDesc.append(
                            "Organization - " + d +
                            " Unit count reached the limit " +
                            "comparing TempDB and MainDB"
                        )
        else:
            mainData = mainStrore.get(
                str(self._legal_entity_id) + "-" + neworgn
            )
            tempData = tempStore.get(
                self._legal_entity_name + "-" + neworgn.strip()
            )
            if tempData is None:
                for temp_d in tempStore:
                    if (
                        temp_d.split('-')[0].strip() ==
                        self._legal_entity_name.strip()
                    ):
                        tempData = tempStore.get(temp_d)
                        orgn_name = tempData.get("organization")
                        temporgn = ''
                        for o in orgn_name.split('>>'):
                            temporgn = temporgn + o.strip() + '>>'
                        temporgn = temporgn[:-2]
                        if neworgn in temporgn.strip():
                            saved_units = saved_units +\
                                int(tempData.get("saved_units"))
            else:
                saved_units = tempData.get("saved_units")
            self.save_csv_domain_orgn_units(
                        self._legal_entity_name, neworgn)
            for data in self._csv_domain_orgn:
                split_val = data.split("-")
                if(
                    split_val[0] ==
                    self._legal_entity_name.strip() and
                    split_val[1] == neworgn.strip()
                ):
                    csv_units = int(split_val[2])
                    break

            if mainData is not None:
                main_temp_units = int(mainData.get("created_units")) +\
                     int(saved_units) + int(csv_units)
                if main_temp_units > mainData.get("total_unit_count"):
                    errDesc.append(
                        "Organization - " + neworgn +
                        " Unit count reached the limit " +
                        "comparing TempDB and MainDB"
                    )
        return '|;|'.join(errDesc)

    def save_csv_domain_orgn_units(self, le_name, domain_org):
        if len(self._csv_domain_orgn) == 0:
            self._csv_domain_orgn.append(
                le_name.strip() + "-" +
                domain_org.strip() + "-1"
            )
        else:
            # join_csv = ','.join(self._csv_domain_orgn)
            # self._csv_domain_orgn = []
            occur = 0
            for i, data in enumerate(self._csv_domain_orgn):
                split_val = data.split("-")
                if(
                    split_val[0] ==
                    le_name.strip() and
                    split_val[1] == domain_org.strip()
                ):
                    occur += 1
                    save_unit = int(
                        split_val[2].strip()) + 1
                    self._csv_domain_orgn.pop(i)
                    self._csv_domain_orgn.append(
                        le_name.strip() +
                        "-" +
                        domain_org.strip() + "-" + str(save_unit)
                    )
                    break
            if occur == 0:
                self._csv_domain_orgn.append(
                    le_name.strip() +
                    "-" +
                    domain_org.strip() + "-" + "1")

    '''
        looped csv data to perform corresponding validation
        returns: valid and invalid return format
        rType: dictionary
    '''

    def perform_csv_temp_validation(self):
        csv_column_compare = None
        csv_column_compare = self.compare_csv_columns()
        if csv_column_compare == "Csv Column Mismatched":
            return csv_column_compare, None, None, None, None
        else:
            csv_unitcode_invalid = self.check_valid_unit_code_in_csv()
            self._error_summary["invalid_data_error"] += \
                csv_unitcode_invalid[0]
            csv_unitcode_duplicate = self.check_duplicate_unit_code_in_csv()
            self._error_summary["duplicate_error"] += csv_unitcode_duplicate[0]
            csv_domain_duplicate = self.check_duplicate_domain_in_csv_row()
            csv_orgn_duplicate = self.check_duplicate_organization_in_csv_row()
            self.get_tempDB_data()
            self._uploaded_by = self._session_user_obj.user_id()
            self.init_values(self._session_user_obj.user_id(), self._client_id)
            return (
                csv_column_compare, csv_unitcode_invalid,
                csv_unitcode_duplicate,
                csv_domain_duplicate, csv_orgn_duplicate
            )

    def bind_unit_code_errors(
        self, csv_unitcode_invalid, csv_unitcode_duplicate, unitCodeErr, v,
        key, res
    ):
        if csv_unitcode_invalid[0] > 0:
            for u in csv_unitcode_invalid[1]:
                if u == v:
                    msg = "%s - %s %s" % (
                        key, v, " Invalid data"
                    )
                    if res is not True:
                        res.append(msg)
                    else:
                        res = [msg]
        if csv_unitcode_duplicate[0] > 0:
            for u in csv_unitcode_duplicate[1]:
                if u == v:
                    msg = "%s - %s" % (
                        key, v + " Duplicated in CSV"
                    )
                    if res is not True:
                        res.append(msg)
                    else:
                        res = [msg]
        unitCodeErr = \
            self.check_duplicate_unit_code_in_tempDB(v)
        if unitCodeErr is not None and unitCodeErr != "":
            if res is not True:
                res.append(unitCodeErr)
            else:
                res = [unitCodeErr]
            self._error_summary["duplicate_error"] += 1
        return res

    def bind_domain_errors(
        self, value, csv_domain_duplicate, domain_row_last, res, i, key
    ):
        if csv_domain_duplicate is not None:
            for d in csv_domain_duplicate:
                if (
                    d == value and domain_row_last != i
                ):
                    domain_row_last = i
                    msg = "%s - %s" % (
                        key, value + " Duplicated in CSV"
                    )
                    if res is not True:
                        res.append(msg)
                    else:
                        res = [msg]
                    self._error_summary[
                        "duplicate_error"] += 1
        return res

    def bind_organization_errors(
        self, orgn_row_last, csv_orgn_duplicate, res, key,
        unitCountErr, value, csv_domain_name
    ):
        if csv_orgn_duplicate is not None:
            for o in csv_orgn_duplicate:
                if o == value:
                    msg = "%s - %s" % (
                        key, value + " Duplicated in CSV"
                    )
                    if res is not True:
                        res.append(msg)
                    else:
                        res = [msg]
                    self._error_summary[
                        "duplicate_error"] += 1
        unitCountErr = \
            self.check_organization_unit_count_in_tempDB(
                value)
        if (
            unitCountErr is not None and unitCountErr != ""
        ):
            if res is not True:
                res.append(unitCountErr)
            else:
                res = [unitCountErr]
            self._error_summary[
                "max_unit_count_error"] += 1
        # check organization under domain
        checkOrgn = \
            self.check_organization_under_domain(
                csv_domain_name, value
            )
        if checkOrgn is not None and checkOrgn != "":
            if res is not True:
                res.append(checkOrgn)
            else:
                res = [checkOrgn]
            self._error_summary[
                "invalid_data_error"] += 1
        return res

    def process_dictionary_values(
        self, key, v, res
    ):
        valid_failed, error_cnt = parse_csv_dictionary_values(
            key, v
        )
        if valid_failed is not True:
            if res is True:
                res = valid_failed
                error_count = error_cnt
            else:
                res.extend(valid_failed)
                self._error_summary[
                        "mandatory_error"] += error_cnt["mandatory"]
                self._error_summary[
                    "max_length_error"] += error_cnt["max_length"]
                self._error_summary[
                    "invalid_char_error"] += error_cnt["invalid_char"]
        return res

    def process_unbound_methods(
        self, v, csvParam, key, res, isFound
    ):
        if v != "":
            if (
                csvParam.get("check_is_exists") is True or
                csvParam.get("check_is_active") is True
            ):
                unboundMethod = \
                    self._validation_method_maps.get(key)
                if unboundMethod is not None:
                    isFound = unboundMethod(v)
            if isFound is not True and isFound != "":
                msg = "%s - %s" % (key, isFound)
                if res is not True:
                    res.append(msg)
                else:
                    res = [msg]

                if "Status" in isFound:
                    self._error_summary["inactive_error"] += 1
                elif "Unit count exceeds" in isFound:
                    self._error_summary[
                        "max_unit_count_error"
                    ] += 1
                else:
                    self._error_summary[
                        "invalid_data_error"] += 1
        return res

    def perform_validation(self):
        mapped_error_dict, mapped_header_dict = {}, {}
        invalid, i = 0, 0
        csv_domain_name = None
        csv_column_compare, csv_unitcode_invalid, csv_unitcode_duplicate, \
            csv_domain_duplicate, csv_orgn_duplicate = \
            self.perform_csv_temp_validation()
        if csv_column_compare is not None:
            return "Csv Column Mismatched"
        print "length validation of file--------------------------------"
        print len(self._source_data), CSV_MAX_LINES
        if len(self._source_data) > 0 and \
                len(self._source_data) <= CSV_MAX_LINES:
            for row_idx, data in enumerate(self._source_data):
                i = row_idx
                res = True
                error_count = {
                    "mandatory": 0, "max_length": 0, "invalid_char": 0
                }
                for key in self._csv_column_name:
                    value = data.get(key)
                    isFound = ""
                    values = value.strip().split(CSV_DELIMITER)
                    csvParam = csv_params.get(key)
                    unitCodeErr = None
                    unitCountErr = None
                    domain_row_last = object()
                    orgn_row_last = object()
                    if (key == "Format" and value != ''):
                        self._doc_names.append(value)
                    for v in [v.strip() for v in values]:
                        if key == "Legal_Entity":
                            self._legal_entity_name = v
                        elif key == "Unit_Code" and v != "auto_gen":
                            res = self.bind_unit_code_errors(
                                csv_unitcode_invalid, csv_unitcode_duplicate,
                                unitCodeErr, v, key, res
                            )
                        elif key == "Postal_Code":
                            if v == "0":
                                msg = "%s - %s" % (key, "invalid Postal Code")
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]
                                self._error_summary["invalid_data_error"] += 1
                        elif key == "Domain":
                            csv_domain_name = value
                            res = self.bind_domain_errors(
                                value, csv_domain_duplicate,
                                domain_row_last, res, i, key
                            )
                        elif key == "Organization" and\
                                orgn_row_last != i:
                            orgn_row_last = i
                            res = self.bind_organization_errors(
                                orgn_row_last, csv_orgn_duplicate, res, key,
                                unitCountErr, value, csv_domain_name
                            )
                        res = self.process_dictionary_values(key, v, res)
                        res = self.process_unbound_methods(
                            v, csvParam, key, res, isFound)
                    if res is not True:
                        err_str = (',').join(res)
                        if err_str.find(key) != -1:
                            head_idx = mapped_header_dict.get(key)
                            if head_idx is None:
                                head_idx = [row_idx]
                            else:
                                head_idx.append(row_idx)
                            mapped_header_dict[key] = head_idx
                if res is not True:
                    error_list = mapped_error_dict.get(row_idx)
                    if error_list is None:
                        error_list = res
                    else:
                        error_list.extend(res)
                    mapped_error_dict[row_idx] = error_list
                    invalid += 1
                    # self._error_summary[
                    #     "mandatory_error"] += error_count["mandatory"]
                    # self._error_summary[
                    #     "max_length_error"] += error_count["max_length"]
                    # self._error_summary[
                    #     "invalid_char_error"] += error_count["invalid_char"]
                    res = True
            if invalid > 0:
                return self.make_invalid_return(
                    mapped_error_dict, mapped_header_dict)
            else:
                return self.make_valid_return(
                    mapped_error_dict, mapped_header_dict)
        else:
            if len(self._source_data) == 0:
                return "Empty CSV File Uploaded"
            elif len(self._source_data) > CSV_MAX_LINES:
                return "CSV File lines reached max limit"

    ##################################################################
    '''
        make_invalid_return: This class method is create the invalid
        file of the uploaded csv file in four formats if required.
    '''
    ##################################################################

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        try:
            fileString = self._csv_name.split('.')
            file_name = "%s_%s.%s" % (
                fileString[0], "invalid", "xlsx"
            )
            final_hearder = self._csv_header
            final_hearder.append("Error Description")
            self.write_client_data_to_excel(
                os.path.join(
                    BULKUPLOAD_INVALID_PATH, "xlsx"
                ), file_name, final_hearder,
                self._source_data, mapped_error_dict,
                mapped_header_dict, self._sheet_name
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
                "invalid_char_error": self._error_summary[
                    "invalid_char_error"],
                "invalid_data_error": self._error_summary[
                    "invalid_data_error"],
                "inactive_error": self._error_summary[
                    "inactive_error"],
                "max_unit_count_error": self._error_summary[
                    "max_unit_count_error"],
                "total": total,
                "invalid": invalid,
                "doc_count": len(set(self._doc_names))
            }
        except Exception, e:
            print str(traceback.format_exc())
            return e

    ###################################################################
    '''
        make_valid_return: This class method is create the valid count
        of the csv file data uploaded.
    '''
    ###################################################################

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

    def write_client_data_to_excel(
        self, file_src_path, file_name, headers, column_data,
        data_error_dict, header_dict, sheet_name
    ):

        file_path = os.path.join(file_src_path, file_name)
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet(sheet_name)
        worksheet.set_column('A:A', 30)
        bold = workbook.add_format({'bold': 1})
        error_format = workbook.add_format({
            'font_color': 'red'
        })
        cells = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
            'W', 'X', 'Y', 'Z'
        ]
        for idx, h in enumerate(headers):
            if idx < 26:
                x = idx
            else:
                x = idx - 26

            c = "%s%s" % (cells[x], 1)
            if (
                h != 'Division' and
                h != 'Category' and
                h != "Error Description"
            ):
                h = "%s%s" % (h, '*')

            worksheet.write(c, h, bold)

        row = 1
        col = 0

        for idx, dat in enumerate(column_data):

            for i, h in enumerate(headers):
                h = h.replace('*', '')
                error_col = header_dict.get(h)
                if error_col is None:
                    error_col = []
                d = dat.get(h)
                if h == "Error Description":
                    error_text = data_error_dict.get(idx)
                    if error_text is None:
                        e = ""
                    else:
                        e = "|;|".join(error_text)
                    # print e
                    # e.encode("utf8")
                    # e.decode('utf8')

                    worksheet.write_string(row, col + i, e)
                else:
                    # d.decode('utf8')
                    try:
                        d.decode("utf8")
                        if idx in error_col:
                            worksheet.write_string(
                                row, col + i, d, error_format
                            )
                        else:
                            worksheet.write_string(row, col + i, d)
                    except Exception, e:
                        worksheet.write_string(row, col + i, d, error_format)
            row += 1

        # summary sheet
        summarySheet = workbook.add_worksheet("summary")
        for idx, h in enumerate(["Field Name", "Count"]):
            c = "%s%s" % (cells[idx], 1)
            summarySheet.write(c, h, bold)

        srow = 1
        for i, col in enumerate(headers[:-1]):

            value = 0
            col = col.replace('*', '')
            error_count = header_dict.get(col)
            if error_count is not None:
                for j in error_count:
                    for k in data_error_dict.get(j):
                        # value = len(error_count)
                        if col in k:
                            value = int(value) + 1
            summarySheet.write(srow, 0, col)
            summarySheet.write(srow, 1, value)
            value = 0
            srow += 1
        workbook.close()

######################################################################
'''
    ValidateClientUnitsBulkDataForApprove: This class is created to
    validate the approved temp db data for further process
'''
######################################################################


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
        self._uploaded_by = None

    ######################################################################
    '''
        get_uploaded_data: This class method is defined to fetch the temp
        database data under the csv id
    '''
    ######################################################################

    def get_uploaded_data(self):
        self._temp_data = self._db.call_proc(
            "sp_bulk_client_unit_by_csvid", [self._csv_id]
        )

    ######################################################################
    '''
        store_initial_values: This class method is defined to store the
        initial values when the user selects reject all option
    '''
    ######################################################################

    def store_initial_values(self):
        for row_idx, data in enumerate(self._temp_data):
            if row_idx == 0:
                self._group_name = data.get("client_group")
                self._csv_name = data.get("csv_name")
                self._uploaded_by = data.get("uploaded_by")
                break

    ######################################################################
    '''
        check_for_system_declination_errors: This class method is defined
        to check the system declination errors during approving/ rejcting
        a group of units
    '''
    ######################################################################

    def check_for_system_declination_errors(self):
        sys_declined_count = 0
        self._declined_bulk_unit_id = []
        self._declined_bulk_unit_id_err = []
        manual_rejection_count = 0
        self.init_values(self._session_user_obj.user_id(), self._client_id)
        for row_idx, data in enumerate(self._temp_data):
            res = True
            if row_idx == 0:
                self._group_name = data.get("client_group")
                self._csv_name = data.get("csv_name")
                self._uploaded_by = data.get("uploaded_by")
            if data.get("action") == 2:
                manual_rejection_count += 1
            for key in self._csv_column_name:
                value = data.get(key)
                if key == "Postal_Code":
                    value = str(value)
                isFound = ""
                if value is None:
                    continue

                csvParam = csv_params.get(key)
                if csvParam is None:
                    continue

                if type(value) is not int:
                    values = value.strip().split(CSV_DELIMITER)

                for v in values:
                    if type(v) is str:
                        v = v.strip()

                    if v != "":
                        if (
                            csvParam.get("check_is_exists") is True or
                            csvParam.get("check_is_active") is True
                        ):
                            unboundMethod = \
                                self._validation_method_maps.get(key)
                            if unboundMethod is not None:
                                isFound = unboundMethod(v)
                        if isFound is not True and isFound != "":
                            msg = "%s - %s" % (key, isFound)
                            if res is not True:
                                res.append(msg)
                            else:
                                res = [msg]
                            sys_declined_count += 1
            if sys_declined_count > 0 and res is not True:
                self._declined_bulk_unit_id.append(data.get("bulk_unit_id"))
                self._declined_bulk_unit_id_err.append(res)
                res = True
        return self._declined_bulk_unit_id, \
            self._declined_bulk_unit_id_err, \
            manual_rejection_count

    ######################################################################
    '''
        process_data_to_main_db_insert: This class method is defined to
        process the data to insert to the master database
    '''
    ######################################################################

    def process_data_to_main_db_insert(self, system_declined_units):
        self._temp_data.sort(key=lambda x: (
            x["Country"], x["Legal_Entity"], x["Division"], x["Category"]
        ))
        for k, v in groupby(self._temp_data, key=lambda s: (
            s["Country"], s["Legal_Entity"], s["Division"], s["Category"]
        )):
            self._auto_unit_code = None
            grouped_list = list(v)
            if len(grouped_list) == 0:
                continue
            value = grouped_list[0]
            le_id = None
            cl_id = self._client_id
            bg_id = self._business_group_id
            c_id = self._country.get(value.get("Country")).get("country_id")
            self._country_id = c_id
            groupName = value.get("client_group")
            created_by = value.get("uploaded_by")
            main_division_id = 0
            main_category_id = 0

            # fetch legal_entity_id

            if self._legal_entity.get(
                str(c_id) + "-" + value.get("Legal_Entity")
            ) is not None:
                le_id = self._legal_entity.get(
                    str(c_id) + "-" + value.get("Legal_Entity")
                ).get("legal_entity_id")

                # fetch division id
                division = value.get("Division")
                if division != '' and self._division.get(
                    str(le_id) + "-" + division
                ) is None:
                    main_division_id = self.save_division(
                        cl_id, le_id, bg_id, division, created_by
                    )
                elif division != '':
                    main_division_id = self._division.get(
                        str(le_id) + "-" + division
                    ).get("division_id")

                # fetch category id
                category = value.get("Category")
                if category != '' and \
                        self._category.get(
                            str(le_id) + "-" + category
                        ) is None:
                    main_category_id = self.save_category(
                        cl_id, le_id, bg_id, main_division_id,
                        category, created_by
                    )
                elif category != '':
                    main_category_id = self._category.get(
                        str(le_id) + "-" + category
                    ).get("category_id")

                self.save_units(
                    cl_id, bg_id, le_id, main_division_id, main_category_id,
                    c_id, groupName, grouped_list,
                    system_declined_units, created_by
                )
        self._auto_unit_code = None

    ######################################################################
    '''
        make_rejection: This class method is defined to process the data
        which are rejected due to system errors.
    '''
    ######################################################################

    def make_rejection(
        self, csv_id, action_type, declined_ids, declined_ids_error
    ):
        try:
            for unit_id, unit_error in zip(declined_ids, declined_ids_error):
                q = "update tbl_bulk_units set action = %s, remarks = %s " + \
                    "where bulk_unit_id = %s"
                self._db.execute_insert(
                    q, [3,
                        str("|;|".join(unit_error)),
                        int(unit_id)
                        ]
                )
            if action_type == 1:
                q = "delete from tbl_bulk_units where action = %s and "\
                    "csv_unit_id = %s"
                self._db.execute_insert(q, [1, int(csv_id)])
            else:
                q = "delete from tbl_bulk_units where action = %s and "\
                    "csv_unit_id = %s"
                self._db.execute_insert(q, [1, int(csv_id)])

                q = "delete from tbl_bulk_units where action = %s and "\
                    "csv_unit_id = %s"
                self._db.execute_insert(q, [2, int(csv_id)])
        except Exception, e:
            print e
            raise ValueError("Transaction failed during system rejection")
