import os
import collections
import traceback
import mysql.connector
import xlsxwriter
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST , KNOWLEDGE_DB_PORT , KNOWLEDGE_DB_USERNAME ,
    KNOWLEDGE_DB_PASSWORD , KNOWLEDGE_DATABASE_NAME ,
    CSV_DELIMITER , BULKUPLOAD_INVALID_PATH, CSV_MAX_LINES
)
from server.common import (
    get_date_time
)
from server.database.forms import (
    frmClientUnitBulkUpload , frmApproveClientUnitBulkUpload
)
from server.exceptionmessage import process_error
from keyvalidationsettings import csv_params, parse_csv_dictionary_values
from ..bulkuploadcommon import (
    rename_file_type
)

__all__ = [
    "ValidateClientUnitsBulkCsvData" ,
    "ValidateClientUnitsBulkDataForApprove"
]
###########################################################################
'''
    SourceDB: This class methods executed with main db connection
    also check csv data validation
'''
##########################################################################


class SourceDB(object) :

    def __init__(self) :

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
        self._auto_unit_code = None
        self._validation_method_maps = {}
        self.statusCheckMethods()
        self.connect_source_db()

    ###########################################################################
    '''
        csv_column_fields: This class methods contains the declaration of csv
        column names matched with the csv file
    '''
    ##########################################################################

    def csv_column_fields(self) :

        self._csv_column_name = [
            "Legal_Entity" , "Division" , "Category" , "Geography_Level" ,
            "Unit_Location" , "Unit_Code" , "Unit_Name" , "Unit_Address" ,
            "City", "State" , "Postal_Code" , "Domain" , "Organization"
        ]

    ###########################################################################
    '''
        connect_source_db: This class methods connects to the main compfie
        knowledge database.
    '''
    ##########################################################################

    def connect_source_db(self) :

        self._source_db_con = mysql.connector.connect(
            user=KNOWLEDGE_DB_USERNAME ,
            password=KNOWLEDGE_DB_PASSWORD ,
            host=KNOWLEDGE_DB_HOST ,
            database=KNOWLEDGE_DATABASE_NAME ,
            port=KNOWLEDGE_DB_PORT ,
            autocommit=False ,
        )
        self._source_db = Database(self._source_db_con)
        self._source_db.begin()

    ###########################################################################
    '''
        close_source_db: This class methods closes the main compfie
        knowledge database.
    '''
    ##########################################################################

    def close_source_db(self) :

        self._source_db.close()
        self._source_db_con.close()

    ###########################################################################
    '''
        init_values: This class methods contains user id and client id as
        parameter to fetch the master db data for validation
    '''
    ##########################################################################

    def init_values(self, user_id, client_id) :

        self.get_legal_entities(user_id, client_id)
        self.get_divisions(client_id)
        self.get_categories(client_id)
        self.get_geography_level(user_id)
        self.get_unit_location()
        self.get_unit_code(client_id)
        self.get_domains_organizations(client_id)

    ###########################################################################
    '''
        get_legal_entities: This class methods contains user id and client id as
        parameter to fetch the master db legal entities under a client user
    '''
    ##########################################################################

    def get_legal_entities(self , user_id , client_id) :

        data = self._source_db.call_proc_with_multiresult_set(
            "sp_bu_legal_entities" , [client_id , user_id] , 2
        )
        for d in data[1] :
            self.Legal_Entity[d["legal_entity_name"]] = d

    ###########################################################################
    '''
        get_divisions: This class methods contains client id as
        parameter to fetch the master db division under a client
    '''
    ##########################################################################

    def get_divisions(self, client_id) :

        data = self._source_db.call_proc("sp_bu_divisions" , [client_id])
        for d in data :
            self.Division[d["division_name"]] = d

    ###########################################################################
    '''
        get_categories: This class methods contains client id as
        parameter to fetch the master db categories under a client
    '''
    ##########################################################################

    def get_categories(self, client_id) :

        data = self._source_db.call_proc("sp_bu_categories" , [client_id])
        for d in data :
            self.Category[d["category_name"]] = d

    ###########################################################################
    '''
        get_geography_level: This class methods contains user id as
        parameter to fetch the master db geography levels under a user
    '''
    ##########################################################################

    def get_geography_level(self , user_id) :

        data = self._source_db.call_proc("sp_bu_geography_levels" , [user_id])
        for d in data :
            self.Geography_Level[str(d["country_id"]) + '-' + d["level_name"]] = d

    ###########################################################################
    '''
        get_unit_location: This class methods used to fetch the master db
        unit location under a level id
    '''
    ##########################################################################

    def get_unit_location(self) :

        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data :
            self.Unit_Location[d["parent_names"]] = d

    ###########################################################################
    '''
        get_unit_code: This class methods contains client id as a parameter
        used to fetch the master db unit code under aa client
    '''
    ##########################################################################

    def get_unit_code(self , client_id) :

        data = self._source_db.call_proc("sp_bu_unit_code" , [client_id])
        for d in data :
            self.Unit_Code[d["unit_code"]] = d

    ###########################################################################
    '''
        get_domains_organizations: This class methods contains client id as a
        parameter used to fetch the master db domain and organization under a
        client id
    '''
    ##########################################################################

    def get_domains_organizations(self , client_id) :

        data = self._source_db.call_proc(
            "sp_bu_domains_organization_unit_count" ,
            [client_id]
        )
        for d in data :
            self.Domain[str(d["legal_entity_id"]) + "-" + d["domain_name"]] = d
            self.Organization[
                str(d["legal_entity_id"]) +
                "-" + d["domain_name"] +
                " >> " + d["organization_name"]
            ] = d

    ######################################################################################
    '''
        check_base: This class methods contains status check value, list of the
        key, key value, field name to check whether the record is active/ inactive

    '''
    #######################################################################################

    def check_base(self , check_status , store, key_name , status_name) :

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

    ######################################################################################
    '''
        check_legal_entity: This class methods contains legal entity name
        to check whether the legal entity is available for transaction

    '''
    #######################################################################################

    def check_legal_entity(self , legal_entity_name) :

        store = self.Legal_Entity
        data = store.get(legal_entity_name)
        if (
            data is not None and
            data.get("is_closed") == 0 and
            data.get("is_approved") == 1 and
            data.get("le_contract_days") >= 0 and
            self._uploaded_by is not None and (self._uploaded_by == data.get("user_id"))
        ):
            self.Legal_Entity_Id = data.get("legal_entity_id")
            self.Country_Id = data.get("country_id")
            self.Business_Group_Id = data.get("business_group_id")
            return self.check_base(False, store, legal_entity_name, None)
        else:
            if data is None :
                return "Not found"
            elif data is not None and (data.get("is_closed") == 1 or data.get("le_contract_days") < 0):
                return "Status Inactive"
            elif data is not None and data.get("is_approved") == 0 :
                return "Not found"
            elif data is not None and (self._uploaded_by is not None and (
                self._uploaded_by != data.get("user_id"))
            ):
                return "Not assigned to the Techno Executive"

    ######################################################################################
    '''
        check_division: This class methods contains division name
        to check whether the division is available for transaction

    '''
    #######################################################################################

    def check_division(self , division_name) :

        store = self.Division
        data = store.get(division_name)
        if data is not None :
            return self.check_base(False , self.Division , division_name , None)
        else :
            return True

    ######################################################################################
    '''
        check_category: This class methods contains category name
        to check whether the category is available for transaction

    '''
    #######################################################################################

    def check_category(self , category_name) :

        store = self.Category
        data = store.get(category_name)
        if data is not None :
            return self.check_base(False , self.Category , category_name , None)
        else:
            return True

    ######################################################################################
    '''
        check_geography_level: This class methods contains geography level name
        to check whether the geography level is available for transaction

    '''
    #######################################################################################

    def check_geography_level(self , level_name) :

        store = self.Geography_Level
        data = store.get(str(self.Country_Id) + '-' + level_name)
        if data is not None :
            if (
                data.get("country_id") == self.Country_Id and
                data.get("level_name") == level_name
            ) :
                self.Level_Id = data.get("level_id")
                return self.check_base(
                    True, self.Geography_Level , (str(self.Country_Id) + '-' + level_name), None
                )
            else :
                return "Not found"
        else:
            return "Not found"

    ######################################################################################
    '''
        check_unit_location: This class methods contains geography name
        to check whether the geography name is available for transaction

    '''
    #######################################################################################

    def check_unit_location(self , geography_name) :

        store = self.Unit_Location
        data = store.get(geography_name)
        if data is not None :
            if (data.get("level_id") == self.Level_Id) :
                return self.check_base(True, self.Unit_Location, geography_name, None)
            else :
                return "Not found"
        else :
            return "Not found"

    ######################################################################################
    '''
        check_unit_code: This class methods contains unit code
        to check whether the unit code is already created under the legal entity

    '''
    #######################################################################################

    def check_unit_code(self , unit_code) :

        if unit_code != "auto_gen" :
            store = self.Unit_Code
            data = store.get(unit_code)
            if data is not None :
                if (data.get("legal_entity_id") != self.Legal_Entity_Id) :
                    return self.check_base(False, self.Unit_Code, unit_code, None)
                else :
                    return "Unit_Code - " + unit_code + " Duplication in Main DB"
            else :
                return True
        else :
            return True

    ######################################################################################
    '''
        check_domain: This class methods contains domain name
        to check whether the domain is under the legal entity

    '''
    #######################################################################################

    def check_domain(self , domain_name) :
        store = self.Domain
        errDesc = []
        status = None
        if domain_name.find(CSV_DELIMITER) > 0 :
            splittedDomain = domain_name.split(CSV_DELIMITER)
            for d in splittedDomain:
                data = store.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if data is not None:
                    status = self.check_base(
                        True, self.Domain , (str(self.Legal_Entity_Id) + "-" + d.strip()) ,
                        "domain_is_active"
                    )
                    if status is "Status Inactive":
                        errDesc.append(d + status)
                else:
                    errDesc.append(d + " Not Found")
        else:
            data = store.get(str(self.Legal_Entity_Id) + "-" + domain_name.strip())
            if data is not None:
                return self.check_base(
                    True , self.Domain , (str(self.Legal_Entity_Id) + "-" + domain_name.strip()),
                    "domain_is_active"
                )
            else:
                errDesc.append(domain_name + " Not Found")

        if len(errDesc) > 0:
            return ','.join(errDesc)

    ######################################################################################
    '''
        check_for_organization_under_domain: This class method is defined
        to check the whether each domain has organization inside a csv row
    '''
    #######################################################################################

    def check_for_organization_under_domain(self, domain_name, orgn_name):
        msg = []
        if domain_name.strip().find(CSV_DELIMITER) >= 0:
            splitDomain = domain_name.split(CSV_DELIMITER)
            for d in splitDomain:
                if orgn_name.find(d.strip()) < 0 :
                    msg.append("Organization - " + d.strip() + " organization is blank")
        else:
            if orgn_name.find(domain_name.strip()) < 0 :
                msg.append("Organization - " + domain_name.strip() + " organization is blank")

        if len(msg) > 0 :
            return ','.join(msg)

    ######################################################################################
    '''
        check_organization: This class methods contains organization name
        to check whether the organization is under the legal entity

    '''
    #######################################################################################

    def check_organization(self , organization_name):
        store = self.Organization
        errDesc = []
        status = None
        if organization_name.find(CSV_DELIMITER) > 0 :
            splittedOrg = organization_name.split(CSV_DELIMITER)
            for d in splittedOrg:
                data = store.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if data is not None :
                    status = self.check_base(
                        True, self.Organization , (str(self.Legal_Entity_Id) + "-" + d.strip()) ,
                        "organization_is_active"
                    )
                    if status is "Status Inactive" :
                        errDesc.append(d.strip() + status)
                    else:
                        if int(data.get("created_units")) >= int(data.get("total_unit_count")):
                            errDesc.append(d.strip() + " Unit count exceeds the limit")
                else:
                    errDesc.append(d.strip() + " Not Found")

        else :
            data = store.get(str(self.Legal_Entity_Id) + "-" + organization_name.strip())
            if data is not None :
                if int(data.get("created_units")) >= int(data.get("total_unit_count")) :
                    errDesc.append(d + " Unit count exceeds the limit")
                else:
                    return self.check_base(
                        True, self.Organization , (str(self.Legal_Entity_Id) + "-" + organization_name.strip()) ,
                        "organization_is_active")
            else :
                errDesc.append(organization_name.strip() + " Not Found")

        if len(errDesc) > 0:
            return ','.join(errDesc)

    def statusCheckMethods(self) :
        self._validation_method_maps = {
            "Legal_Entity" : self.check_legal_entity ,
            "Division" : self.check_division ,
            "Category" : self.check_category ,
            "Geography_Level" : self.check_geography_level ,
            "Unit_Location" : self.check_unit_location ,
            "Unit_Code" : self.check_unit_code ,
            "Domain" : self.check_domain ,
            "Organization" : self.check_organization
        }

    ######################################################################################
    '''
        save_division: This class methods is defined to store the division under client
        in master DB
    '''
    #######################################################################################

    def save_division(self , cl_id , le_id , bg_id , division_name , createdby) :

        created_on = get_date_time()
        if bg_id is not None :
            bg_id = int(bg_id)
        else:
            bg_id = None
        insert_value = [
            int(cl_id) , int(le_id) ,
            bg_id , division_name ,
            int(createdby) , str(created_on)
        ]
        q = "INSERT INTO tbl_divisions (client_id, legal_entity_id, " + \
            " business_group_id, division_name, created_by, created_on) values " + \
            " (%s, %s, %s, %s, %s, %s)"
        division_id = self._source_db.execute_insert(
            q, insert_value
        )
        if division_id is False :
            raise process_error("E054")
        return division_id

    ######################################################################################
    '''
        save_category: This class methods is defined to store the category under client
        in master DB
    '''
    #######################################################################################

    def save_category(
        self, cl_id, le_id, bg_id, division_id, category_name, createdby
    ) :

        created_on = get_date_time()
        if bg_id is not None :
            bg_id = int(bg_id)
        else :
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
        if category_id is False :
            raise process_error("E093")
        return category_id

    ######################################################################################
    '''
        generate_unit_code: This class methods is defined to generate unit code
        in master DB
    '''
    #######################################################################################

    def generate_unit_code(self , cl_id , grp_name) :

        unit_code_start_letters = grp_name[:2].upper()
        select_param = [
            str(unit_code_start_letters),
            str(unit_code_start_letters),
            int(cl_id)
        ]
        unit_code = None
        q = "SELECT (max(TRIM(LEADING %s FROM unit_code))+1) as code " + \
            "FROM tbl_units WHERE unit_code like binary concat( %s,'%') and " + \
            "CHAR_LENGTH(unit_code) = 7 and client_id=%s; "
        uc = self._source_db.select_one(
            q, select_param
        )
        u_code = int(uc["code"])

        if uc is False :
            raise process_error("E056")
        else:
            if (u_code > 0 and u_code < 10) :
                unit_code = str(unit_code_start_letters) + '0000' + str(u_code)
            elif (u_code >= 10 and u_code < 100) :
                unit_code = str(unit_code_start_letters) + '000' + str(u_code)
            elif (u_code >= 100 and u_code < 1000) :
                unit_code = str(unit_code_start_letters) + '00' + str(u_code)
            elif (u_code >= 1000 and u_code < 10000) :
                unit_code = str(unit_code_start_letters) + '0' + str(u_code)
        return unit_code

    ######################################################################################
    '''
        save_units: This class methods is defined to save the units
        in master DB
    '''
    #######################################################################################

    def save_units(
        self , cl_id , bg_id , le_id , division_id , category_id ,
        country_id , groupName , data , system_declined_units, createdby
    ):

        created_on = get_date_time()
        inserted_records = 0

        # Fetch Other column ID's thru grouped list data
        columns = [
            "client_id", "business_group_id", "legal_entity_id",
            "division_id", "category_id", "country_id",
            "geography_id", "unit_code", "unit_name", "address",
            "postal_code", "is_approved", "approved_by", "approved_on",
            "created_by", "created_on"
        ]
        values = []
        domain_orgn_ids = []
        auto_gen_ids = []
        auto_gen_data = {}
        for idx, d in enumerate(data) :
            if (
                (len(system_declined_units) == 0 or (len(system_declined_units) > 0 and d["bulk_unit_id"] not in system_declined_units)) and
                (int(d["action"]) == 1 or int(d["action"]) == 0)
            ):
                if d["Unit_Code"] == "auto_gen" :
                    auto_gen_ids.append(d["bulk_unit_id"])
                    auto_gen_data[d["bulk_unit_id"]] = d
                else:
                    unit_code = str(d["Unit_Code"]).strip()
                    if bg_id is not None :
                        bg_id = int(bg_id)
                    else:
                        bg_id = None

                    unit_name = d["Unit_Name"]
                    unit_address = d["Unit_Address"] + "," + d["City"] + "," + d["State"]
                    post_code = d["Postal_Code"]

                    main_geo_id = None
                    geo_level_id = self.Geography_Level.get(
                        str(country_id)+"-"+d["Geography_Level"]
                    ).get("level_id")
                    ul = d["Unit_Location"]
                    if geo_level_id == self.Unit_Location.get(ul).get("level_id"):
                        main_geo_id = self.Unit_Location.get(ul).get("geography_id")

                    if d["Organization"].find(CSV_DELIMITER) > 0 :
                        for orgn in d["Organization"].strip().split(CSV_DELIMITER) :
                            split_org = orgn.split(">>")
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self.Domain.get(
                                        str(le_id) + "-" + split_org[0].strip()
                                    ).get("domain_id")) + "-" +
                                str(
                                    self.Organization.get(str(le_id) + "-" + orgn.strip())
                                    .get("organisation_id")
                                )
                            )
                    else :
                        domain = d["Domain"].strip()
                        orgn = d["Organization"].strip()
                        split_org = orgn.split(">>")
                        if domain == split_org[0].strip() :
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self.Domain.get(str(le_id) + "-" + domain).get("domain_id")
                                ) + "-" +
                                str(
                                    self.Organization.get(str(le_id)+"-"+orgn).get("organisation_id"))
                                )

                    self._auto_unit_code = unit_code
                    values.append((
                        int(cl_id) , bg_id , int(le_id) , int(division_id) , int(category_id) ,
                        int(country_id) , int(main_geo_id) , str(unit_code) , str(unit_name) ,
                        str(unit_address) , str(post_code) , 1, int(createdby) , str(created_on),
                        int(createdby) , str(created_on)
                    ))
                    inserted_records += 1

        if values :
            self._source_db.bulk_insert("tbl_units" , columns , values)
            last_id = str(self._auto_unit_code) + ";" + str(inserted_records)
            self.save_units_domain_organizations(last_id , cl_id , domain_orgn_ids)

        # To generate unit codes for all the auto_gen values from csv
        if len(auto_gen_ids) > 0:
            inserted_records = 0
            values = []
            incre = 1
            domain_orgn_ids = []
            for b_u_id in auto_gen_ids:
                unit_data = auto_gen_data.get(b_u_id)
                if unit_data is not None:
                    if bg_id is not None :
                        bg_id = int(bg_id)
                    else:
                        bg_id = None

                    unit_name = unit_data.get("Unit_Name")
                    unit_address = unit_data.get("Unit_Address") + "," + unit_data.get("City") + "," + unit_data.get("State")
                    post_code = unit_data.get("Postal_Code")
                    u_code = int(self._auto_unit_code[2:]) + incre
                    unit_code_start_letters = groupName[:2].upper()

                    if (u_code > 0 and u_code < 10) :
                        unit_code = str(unit_code_start_letters) + '0000' + str(u_code)
                    elif (u_code >= 10 and u_code < 100) :
                        unit_code = str(unit_code_start_letters) + '000' + str(u_code)
                    elif (u_code >= 100 and u_code < 1000) :
                        unit_code = str(unit_code_start_letters) + '00' + str(u_code)
                    elif (u_code >= 1000 and u_code < 10000) :
                        unit_code = str(unit_code_start_letters) + '0' + str(u_code)
                    main_geo_id = None
                    geo_level_id = self.Geography_Level.get(
                        str(country_id)+"-"+unit_data.get("Geography_Level")
                    ).get("level_id")
                    ul = unit_data.get("Unit_Location")
                    if geo_level_id == self.Unit_Location.get(ul).get("level_id"):
                        main_geo_id = self.Unit_Location.get(ul).get("geography_id")

                    if unit_data.get("Organization").find(CSV_DELIMITER) > 0 :
                        for orgn in unit_data.get("Organization").strip().split(CSV_DELIMITER) :
                            split_org = orgn.split(">>")
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self.Domain.get(
                                        str(le_id) + "-" + split_org[0].strip()
                                    ).get("domain_id")) + "-" +
                                str(
                                    self.Organization.get(str(le_id) + "-" + orgn.strip())
                                    .get("organisation_id")
                                )
                            )
                    else :
                        domain = unit_data.get("Domain").strip()
                        orgn = unit_data.get("Organization").strip()
                        split_org = orgn.split(">>")
                        if domain == split_org[0].strip() :
                            domain_orgn_ids.append(
                                str(unit_code) + "-" +
                                str(
                                    self.Domain.get(str(le_id) + "-" + domain).get("domain_id")
                                ) + "-" +
                                str(
                                    self.Organization.get(str(le_id)+"-"+orgn).get("organisation_id"))
                                )

                    values.append((
                        int(cl_id) , bg_id , int(le_id) , int(division_id) , int(category_id) ,
                        int(country_id) , int(main_geo_id) , str(unit_code) , str(unit_name) ,
                        str(unit_address) , str(post_code) , 1, int(createdby) , str(created_on),
                        int(createdby) , str(created_on)
                    ))
                    self._auto_unit_code = unit_code
                    inserted_records += 1
                    # incre += 1

        if values :
            self._source_db.bulk_insert("tbl_units" , columns , values)
            last_id = str(self._auto_unit_code) + ";" + str(inserted_records)
            self.save_units_domain_organizations(last_id , cl_id , domain_orgn_ids)

    ######################################################################################
    '''
        save_units_domain_organizations: This class methods is defined to save the
        domains and organizations under a unit in master DB
    '''
    #######################################################################################

    def save_units_domain_organizations(self , last_id , client_id , domain_orgn_ids) :
        splitLastID = last_id.split(";")
        q = "SELECT unit_id as max_id from tbl_units where unit_code = %s; "
        u_id = self._source_db.select_one(q, [splitLastID[0].strip(), ])
        if int(splitLastID[1].strip()) < int(u_id["max_id"]) :
            unit_start_id = int(u_id["max_id"]) - int(splitLastID[1].strip())
        else:
            unit_start_id = int(splitLastID[1].strip()) - int(u_id["max_id"])

        columns = ["unit_id", "domain_id", "organisation_id"]
        values = []
        unit_id = unit_start_id
        last = object()
        for d_o in domain_orgn_ids :
            u_code = d_o.split("-")[0].strip()
            if last != u_code:
                unit_id = unit_id + 1
                last = u_code
                domain_id = d_o.split("-")[1].strip()
                org_id = d_o.split("-")[2].strip()
                values.append((unit_id , int(domain_id) , int(org_id)))
            else:
                domain_id = d_o.split("-")[1].strip()
                org_id = d_o.split("-")[2].strip()
                values.append((unit_id , int(domain_id) , int(org_id)))
        if values :
            self._source_db.bulk_insert("tbl_units_organizations", columns, values)

    ######################################################################################
    '''
        save_executive_message: This class methods is defined to save the notification message to
        techno manager and compfie admin by techno executive
    '''
    #######################################################################################

    def save_executive_message(self , csv_name , groupname , createdby) :
        # Message for techno manager
        msg_user_id = []
        text = "Client Unit file %s of %s uploaded for  your approval" % (
                csv_name , groupname ,
            )
        link = "/knowledge/approve_client_unit_bu"

        q = "select t1.user_id from tbl_user_login_details as t1 " + \
            " inner join tbl_user_mapping as t2 on t2.parent_user_id = t1.user_id " + \
            " where t1.is_active = 1 and t2.child_user_id = %s "

        row = self._source_db.select_all(q, [createdby])

        for r in row :
            msg_user_id.append(r["user_id"])

        if msg_user_id is not None :
            self._source_db.save_toast_messages(
                5, "Client Unit Bulk Upload", text, link, msg_user_id, createdby
            )

        q1 = "select user_id from tbl_user_login_details where " + \
            "is_active = 1 and user_category_id = 1"

        row1 = self._source_db.select_all(q1)
        c_admin = []
        for r in row1 :
            c_admin.append(r["user_id"])

        if len(c_admin) > 0 :
            self._source_db.save_toast_messages(
                1, "Client Unit Bulk Upload", text, link, c_admin, createdby
            )

        action = "Client Unit csv file uploaded %s of %s " % (
            csv_name, groupname
        )
        self._source_db.save_activity(
            createdby , frmClientUnitBulkUpload , action
        )

    ######################################################################################
    '''
        save_manager_message: This class methods is defined to save the notification message to
        techno executive and compfie admin by techno manager
    '''
    #######################################################################################

    def save_manager_message(self , a_type , csv_name , groupname , createdby , uploaded_by) :
        if a_type == 1 :
            action_type = "approved"
        else :
            action_type = "rejected"

        # Message for techno executive
        msg_user_id = []
        text = "Client Unit file %s of %s has been %s" % (
                csv_name, groupname, action_type
            )
        link = "/knowledge/client-unit-bu"
        msg_user_id.append(uploaded_by)
        self._source_db.save_toast_messages(
            6 , "Approve Client Unit Bulk Upload" , text , link , msg_user_id , createdby
        )

        q1 = "select user_id from tbl_user_login_details where is_active = 1 and user_category_id = 1"
        row1 = self._source_db.select_all(q1)
        c_admin = []
        for r in row1 :
            c_admin.append(r["user_id"])

        if len(c_admin) > 0 :
            self._source_db.save_toast_messages(
                1, "Approve Client Unit Bulk Upload", text, link, c_admin, createdby
            )

        action = "Client Unit file  %s of %s has been %s" % (
            csv_name, groupname, action_type
        )
        self._source_db.save_activity(
            createdby , frmApproveClientUnitBulkUpload , action
        )

    ######################################################################################
    '''
        source_commit: This class methods is defined to commit the transaction made in
        master database
    '''
    #######################################################################################

    def source_commit(self) :
        self._source_db.commit()

######################################################################################
'''
    ValidateClientUnitsBulkCsvData: This class is defined to validate the client unit
    bulk csv data for any system declination error
'''
#######################################################################################

class ValidateClientUnitsBulkCsvData(SourceDB) :
    def __init__(
        self , db , source_data , session_user , client_id , csv_name , csv_header
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
        self._legal_entity_name = None
        self._valid_unit_count = 0
        self._doc_names = []
        self._sheet_name = "Client Unit"

    ######################################################################################
    '''
        errorSummary: This class method is defined to store errors as per the category of
        the error
    '''
    #######################################################################################

    def errorSummary(self) :
        self._error_summary = {
            "mandatory_error" : 0 ,
            "max_length_error" : 0 ,
            "duplicate_error" : 0 ,
            "invalid_char_error" : 0 ,
            "invalid_data_error" : 0 ,
            "inactive_error" : 0 ,
            "max_unit_count_error" : 0
        }

    ######################################################################################
    '''
        compare_csv_columns: This class method is defined to compare the csv coulmns
        header names with the self defined headers
    '''
    #######################################################################################

    def compare_csv_columns(self) :
        res = collections.Counter(self._csv_column_name) == collections.Counter(self._csv_header)
        if res is False :
            raise ValueError("Csv Column Mismatched")

    ######################################################################################
    '''
        check_duplicate_in_csv: This class method is defined to check duplicate values
        inside csv data
    '''
    #######################################################################################

    def check_duplicate_in_csv(self) :
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen :
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Csv data Duplicate Found")

    ######################################################################################
    '''
        check_duplicate_unit_code_in_csv: This class method is defined to check the
        duplication of unit code in csv data
    '''
    #######################################################################################

    def check_duplicate_unit_code_in_csv(self) :
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"] , x["Unit_Code"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s : (
            s["Legal_Entity"] , s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1 and grouped_list[0].get("Unit_Code") != "auto_gen" :
                msg.append(grouped_list[0].get("Unit_Code"))

        if len(msg) > 0 :
            error_msg = "Duplicate unit code found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    ######################################################################################
    '''
        check_duplicate_domain_in_csv_row: This class method is defined to check the
        duplication of domain in a csv row
    '''
    #######################################################################################

    def check_duplicate_domain_in_csv_row(self) :
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"] , x["Domain"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s : (
            s["Legal_Entity"] , s["Domain"]
        )):
            grouped_list = list(v)
            occur = 0
            if grouped_list[0].get("Domain").find('|;|') >= 0 :
                splitDomain = grouped_list[0].get("Domain").split('|;|')
                last = object()
                for val in splitDomain :
                    if last != val :
                        last = val
                    else:
                        occur += 1
            if occur > 0 :
                msg.append(grouped_list[0].get("Domain"))

        if len(msg) > 0 :
            error_msg = "Duplicate Domain found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    ######################################################################################
    '''
        check_duplicate_organization_in_csv_row: This class method is defined to check the
        duplication of organization inside a csv row
    '''
    #######################################################################################

    def check_duplicate_organization_in_csv_row(self) :
        self._source_data.sort(key=lambda x: (
            x["Legal_Entity"] , x["Organization"]
        ))
        msg = []
        for k, v in groupby(self._source_data, key=lambda s : (
            s["Legal_Entity"] , s["Organization"]
        )):
            grouped_list = list(v)
            occur = 0
            if grouped_list[0].get("Organization").find('|;|') >= 0 :
                splitOrgn = grouped_list[0].get("Organization").split('|;|')
                last = object()
                for val in splitOrgn :
                    if last != val :
                        last = val
                    else:
                        occur += 1
            if occur > 0 :
                msg.append(grouped_list[0].get("Organization"))

        if len(msg) > 0 :
            error_msg = "Duplicate Organization found in csv %s" % (
                ','.join(msg)
            )
            raise ValueError(str(error_msg))

    ######################################################################################
    '''
        get_tempDB_data: This class method is defined to fetch the temp db data stored
        under a group/ legal entity and the domain/ organization created under the
        legal entity
    '''
    #######################################################################################

    def get_tempDB_data(self) :

        # To get the unit codes under legal entity
        res = self._db.call_proc("sp_groups_client_units_list" , [self._client_id])
        for d in res:
            self._temp_client_units[d["legal_entity"] + "-" + d["unit_code"]] = d

        # To get the domains, organization and its count under legal entity
        res = self._db.call_proc("sp_get_domain_organization_count" , [self._client_id])
        for d in res:
            self._temp_units_count[d["legal_entity"] + "-" + d["organization"]] = d

    ######################################################################################
    '''
        check_duplicate_unit_code_in_tempDB: This class method is defined to check the
        unit code duplication in temp db
    '''
    #######################################################################################

    def check_duplicate_unit_code_in_tempDB(self, unit_code) :
        tempStore = self._temp_client_units
        data = tempStore.get(self._legal_entity_name + "-" + unit_code)
        if data is not None :
            return "Unit_Code - " + unit_code + " duplication " + "in TempDB "

    ######################################################################################
    '''
        check_organization_unit_count_in_tempDB: This class method is defined to check the
        organization's unit count under a legal entity
    '''
    #######################################################################################

    def check_organization_unit_count_in_tempDB(self , organization_name) :
        mainStrore = self.Organization
        tempStore = self._temp_units_count
        tempData = tempStore.get(
            self._legal_entity_name + "-" + organization_name.strip()
        )
        errDesc = []
        if organization_name.find(CSV_DELIMITER) > 0 :
            splittedOrg = organization_name.split(CSV_DELIMITER)
            for d in splittedOrg :
                mainData = mainStrore.get(str(self.Legal_Entity_Id) + "-" + d.strip())
                if mainData is not None and tempData is not None :
                    main_temp_units = int(
                        mainData.get("total_unit_count")
                    ) - (int(mainData.get("created_units")) + int(tempData.get("saved_units")))
                    if main_temp_units == 0 :
                        errDesc.append("Organization - " + d + " Unit count reached the limit")
                    else:
                        if self._valid_unit_count > main_temp_units :
                            errDesc.append("Organization - " + d + " Unit count reached the limit")
                        else:
                            self._valid_unit_count += 1
        else:
            mainData = mainStrore.get(
                str(self.Legal_Entity_Id) + "-" + organization_name
            )
            tempData = tempStore.get(
                self._legal_entity_name + "-" + organization_name
            )
            if mainData is not None and tempData is not None :
                main_temp_units = int(
                    mainData.get("total_unit_count")
                ) - (int(mainData.get("created_units")) + int(tempData.get("saved_units")))
                if main_temp_units == 0 :
                    errDesc.append("Organization - " + organization_name + " Unit count reached the limit")
                else:
                    if self._valid_unit_count > main_temp_units :
                        errDesc.append("Organization - " + organization_name + " Unit count reached the limit")
                    else:
                        self._valid_unit_count += 1
        return '|;|'.join(errDesc)

    '''
        looped csv data to perform corresponding validation
        returns : valid and invalid return format
        rType: dictionary
    '''

    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        csv_domain_name = None
        self.compare_csv_columns()
        # self.check_duplicate_in_csv()
        self.check_duplicate_unit_code_in_csv()
        self.check_duplicate_domain_in_csv_row()
        self.check_duplicate_organization_in_csv_row()
        self.get_tempDB_data()
        self._uploaded_by = self._session_user_obj.user_id()
        self.init_values(self._session_user_obj.user_id(), self._client_id)
        print "length validation of file-----------------------------------------------"
        print len(self._source_data), CSV_MAX_LINES
        if len(self._source_data) > 0 and len(self._source_data) <= CSV_MAX_LINES:
            for row_idx, data in enumerate(self._source_data) :
                res = True
                error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
                for key in self._csv_column_name :
                    value = data.get(key)
                    isFound = ""
                    values = value.strip().split(CSV_DELIMITER)
                    csvParam = csv_params.get(key)
                    unitCodeErr = None
                    unitCountErr = None

                    if (key == "Format" and value != '') :
                        self._doc_names.append(value)
                    for v in [v.strip() for v in values] :
                        if key == "Legal_Entity":
                            self._legal_entity_name = v
                        elif key == "Unit_Code" and v != "auto_gen" :
                            unitCodeErr = self.check_duplicate_unit_code_in_tempDB(v)
                            if unitCodeErr is not None and unitCodeErr != "":
                                if res is not True :
                                    res.append(unitCodeErr)
                                else:
                                    res = [unitCodeErr]
                                self._error_summary["duplicate_error"] += 1
                        elif key == "Postal_Code" :
                            if v == "0" :
                                msg = "%s - %s" % (key, "invalid Postal Code")
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]
                        elif key == "Domain":
                            csv_domain_name = value
                        elif key == "Organization" :
                            unitCountErr = self.check_organization_unit_count_in_tempDB(value)
                            if unitCountErr is not None and unitCountErr != "":
                                if res is not True:
                                    res.append(unitCountErr)
                                else:
                                    res = [unitCountErr]
                                self._error_summary["max_unit_count_error"] += 1

                            # check organization under domain
                            checkOrgn = self.check_for_organization_under_domain(csv_domain_name, value)
                            if checkOrgn is not None and checkOrgn != "":
                                if res is not True :
                                    res.append(checkOrgn)
                                else:
                                    res = [checkOrgn]
                                self._error_summary["invalid_data_error"] += 1

                        valid_failed, error_cnt = parse_csv_dictionary_values(
                            key, v
                        )
                        if valid_failed is not True :
                            if res is True:
                                res = valid_failed
                                error_count = error_cnt
                            else:
                                res.extend(valid_failed)
                                error_count["mandatory"] += error_cnt["mandatory"]
                                error_count["max_length"] += error_cnt["max_length"]
                                error_count["invalid_char"] += error_cnt["invalid_char"]
                        if v != "":
                            if (
                                csvParam.get("check_is_exists") is True or
                                csvParam.get("check_is_active") is True
                            ):
                                unboundMethod = self._validation_method_maps.get(key)
                                if unboundMethod is not None :
                                    isFound = unboundMethod(v)
                            if isFound is not True and isFound != "":
                                msg = "%s - %s" % (key, isFound)
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]

                                if "Status" in isFound:
                                    self._error_summary["inactive_error"] += 1
                                else:
                                    # if key != "Division" and key != "Category" and key != "Unit_Code":
                                    self._error_summary["invalid_data_error"] += 1

                    if res is not True :
                        err_str = (',').join(res)
                        if err_str.find(key) != -1 :
                            head_idx = mapped_header_dict.get(key)
                            if head_idx is None :
                                head_idx = [row_idx]
                            else:
                                head_idx.append(row_idx)

                            mapped_header_dict[key] = head_idx

                if res is not True :
                    # mapped_error_dict[row_idx] = CSV_DELIMITER.join(res)
                    error_list = mapped_error_dict.get(row_idx)
                    if error_list is None :
                        error_list = res
                    else :
                        error_list.extend(res)

                    mapped_error_dict[row_idx] = error_list

                    invalid += 1
                    self._error_summary["mandatory_error"] += error_count["mandatory"]
                    self._error_summary["max_length_error"] += error_count["max_length"]
                    self._error_summary["invalid_char_error"] += error_count["invalid_char"]
                    res = True

            if invalid > 0 :
                return self.make_invalid_return(mapped_error_dict, mapped_header_dict)
            else :
                return self.make_valid_return(mapped_error_dict, mapped_header_dict)
        else:
            if len(self._source_data) == 0:
                return "Empty CSV File Uploaded"
            elif len(self._source_data) > CSV_MAX_LINES:
                return "CSV File lines reached max limit"

    ######################################################################################
    '''
        make_invalid_return: This class method is create the invalid file of the uploaded
        csv file in four formats if required.
    '''
    #######################################################################################

    def make_invalid_return(self, mapped_error_dict, mapped_header_dict) :
        try:
            fileString = self._csv_name.split('.')
            file_name = "%s_%s.%s" % (
                fileString[0], "invalid", "xlsx"
            )
            final_hearder = self._csv_header
            final_hearder.append("Error Description")
            self.write_client_data_to_excel(
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
                "max_unit_count_error": self._error_summary["max_unit_count_error"],
                "total": total,
                "invalid": invalid,
                "doc_count": len(set(self._doc_names))
            }
        except Exception, e :
            print str(traceback.format_exc())
            return e

    ######################################################################################
    '''
        make_valid_return: This class method is create the valid count of the csv file
        data uploaded.
    '''
    #######################################################################################

    def make_valid_return(self, mapped_error_dict, mapped_header_dict) :
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
            if idx < 26 :
                x = idx
            else :
                x = idx - 26

            c = "%s%s" % (cells[x], 1)
            worksheet.write(c, h, bold)

        row = 1
        col = 0

        for idx, dat in enumerate(column_data):

            for i, h in enumerate(headers):
                h = h.replace('*', '')
                error_col = header_dict.get(h)
                if error_col is None :
                    error_col = []
                d = dat.get(h)
                if h == "Error Description" :
                    error_text = data_error_dict.get(idx)
                    if error_text is None :
                        e = ""
                    else :
                        e = "|;|".join(error_text)
                    print e
                    # e.encode("utf8")
                    # e.decode('utf8')

                    worksheet.write_string(row, col+i, e)
                else :
                    # d.decode('utf8')
                    d.decode("utf8")
                    if idx in error_col :
                        worksheet.write_string(row, col+i, d, error_format)
                    else :
                        worksheet.write_string(row, col+i, d)

            row += 1

        # summary sheet
        summarySheet = workbook.add_worksheet("summary")
        for idx, h in enumerate(["Field Name", "Count"]):
            c = "%s%s" % (cells[idx], 1)
            summarySheet.write(c, h, bold)

        srow = 1
        for i, col in enumerate(headers[:-1]) :
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

###############################################################################################
'''
    ValidateClientUnitsBulkDataForApprove: This class is created to validate the approved temp
    db data for further process
'''
###############################################################################################

class ValidateClientUnitsBulkDataForApprove(SourceDB) :
    def __init__(self, db, csv_id, client_id, session_user) :
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

    ###############################################################################################
    '''
        get_uploaded_data: This class method is defined to fetch the temp database data under
        the csv id
    '''
    ###############################################################################################

    def get_uploaded_data(self) :
        self._temp_data = self._db.call_proc(
            "sp_bulk_client_unit_by_csvid" , [self._csv_id]
        )

    ###############################################################################################
    '''
        store_initial_values: This class method is defined to store the initial values when the user
        selects reject all option
    '''
    ###############################################################################################

    def store_initial_values(self) :
        for row_idx, data in enumerate(self._temp_data) :
            if row_idx == 0 :
                self._group_name = data.get("client_group")
                self._csv_name = data.get("csv_name")
                self._uploaded_by = data.get("uploaded_by")
                break

    ###############################################################################################
    '''
        check_for_system_declination_errors: This class method is defined to check the system
        declination errors during approving/ rejcting a group of units
    '''
    ###############################################################################################

    def check_for_system_declination_errors(self) :
        sys_declined_count = 0
        self._declined_bulk_unit_id = []
        self._declined_bulk_unit_id_err = []
        self.init_values(self._session_user_obj.user_id(), self._client_id)

        for row_idx, data in enumerate(self._temp_data) :
            res = True
            if row_idx == 0 :
                self._group_name = data.get("client_group")
                self._csv_name = data.get("csv_name")
                self._uploaded_by = data.get("uploaded_by")

            for key in self._csv_column_name :
                value = data.get(key)
                if key == "Postal_Code" :
                    value = str(value)
                isFound = ""
                if value is None :
                    continue

                csvParam = csv_params.get(key)
                if csvParam is None :
                    continue

                if type(value) is not int :
                    values = value.strip().split(CSV_DELIMITER)

                for v in values :
                    if type(v) is str :
                        v = v.strip()

                    if v != "" :
                        if (
                            csvParam.get("check_is_exists") is True or
                            csvParam.get("check_is_active") is True
                        ):
                            unboundMethod = self._validation_method_maps.get(key)
                            if unboundMethod is not None :
                                isFound = unboundMethod(v)
                        if isFound is not True and isFound != "" :
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
        return self._declined_bulk_unit_id, self._declined_bulk_unit_id_err

    ###############################################################################################
    '''
        process_data_to_main_db_insert: This class method is defined to process the data to insert
        to the master database
    '''
    ###############################################################################################

    def process_data_to_main_db_insert(self, system_declined_units) :
        self._temp_data.sort(key=lambda x : (
             x["Legal_Entity"], x["Division"], x["Category"]
        ))
        for k, v in groupby(self._temp_data, key=lambda s : (
            s["Legal_Entity"], s["Division"], s["Category"]
        )):
            grouped_list = list(v)
            print "group lengtjh"
            print len(grouped_list)
            if len(grouped_list) == 0 :
                continue
            value = grouped_list[0]
            le_id = None
            cl_id = self._client_id
            bg_id = self.Business_Group_Id
            c_id = self.Country_Id
            groupName = value.get("client_group")
            created_by = value.get("uploaded_by")
            main_division_id = None
            main_category_id = None

            # fetch legal_entity_id
            if self.Legal_Entity.get(value.get("Legal_Entity")) is not None :
                le_id = self.Legal_Entity.get(value.get("Legal_Entity")).get("legal_entity_id")

                # fetch division id
                division = value.get("Division")
                if self.Division.get(division) is None :
                    main_division_id = self.save_division(
                        cl_id, le_id, bg_id, division, created_by
                    )
                else:
                    main_division_id = self.Division.get(division).get("division_id")

                # fetch category id
                category = value.get("Category")
                if self.Category.get(category) is None :
                    main_category_id = self.save_category(
                        cl_id, le_id, bg_id, main_division_id, category, created_by
                    )
                else:
                    main_category_id = self.Category.get(category).get("category_id")

                self.save_units(
                    cl_id, bg_id, le_id, main_division_id, main_category_id,
                    c_id, groupName, grouped_list, system_declined_units, created_by
                )
        self._auto_unit_code = None

    ###############################################################################################
    '''
        make_rejection: This class method is defined to process the data which are rejected due to
        system errors.
    '''
    ###############################################################################################

    def make_rejection(self, csv_id, declined_ids, declined_ids_error) :
        try :
            for unit_id, unit_error in zip(declined_ids, declined_ids_error) :
                q = "update tbl_bulk_units set action = %s, remarks = %s where bulk_unit_id = %s"
                self._db.execute_insert(q, [3, str("|;|".join(unit_error)), int(unit_id)])
            q = "delete from tbl_bulk_units where action = %s and csv_unit_id = %s"
            self._db.execute_insert(q, [1, int(csv_id)])
        except Exception, e :
            print e
            raise ValueError("Transaction failed during system rejection")
