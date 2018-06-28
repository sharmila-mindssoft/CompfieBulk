
import os
import collections
import mysql.connector
from server.exceptionmessage import process_error
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
)
from bulkupload.bulkconstants import (
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH,
    BULK_UPLOAD_DB_HOST, BULK_UPLOAD_DB_PORT, BULK_UPLOAD_DB_USERNAME,
    BULK_UPLOAD_DB_PASSWORD, BULK_UPLOAD_DATABASE_NAME
)
from server.database.forms import (
    frmAssignStatutoryBulkUpload,
    frmApproveAssignStatutoryBulkUpload
)
from keyvalidationsettings import (
    csv_params_as, parse_csv_dictionary_values_as
)
from ..bulkuploadcommon import (
    write_data_to_excel, rename_file_type
)
from server.common import (
    get_date_time
)
from ..budatabase.buassignstatutorydb import (
    get_country_name_by_legal_entity_id
)

__all__ = [
    "ValidateAssignStatutoryCsvData",
    "ValidateAssignStatutoryForApprove"
]
################################
'''
    SourceDB: This class methods executed with main db connection
    also check csv data validation
'''
################################


class SourceDB(object):
    def __init__(self):
        self._source_db = None
        self._source_db_con = None
        self._client_group_ = {}
        self._country_ = {}
        self._legal_entity_ = {}
        self._domain = {}
        self._unit_location = {}
        self._unit_code = {}
        self._unit_name = {}
        self._statutories = {}
        self._child_statutories = {}
        self._statutory_provision = {}
        self._compliance_task = {}
        self._compliance_description = {}
        self._organisation = {}
        self._applicable_status = {}
        self.connect_source_db()
        self._validation_maps = {}
        self.statusCheckMethods()
        self._csv_column_name = []
        self.csv_column_fields()
        self._assigned_compliances_knowledge = []
        self._compliance_info = {}

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

    def init_values(self, user_id, client_id, country_id, legal_entity_id):
        self.get_client_groups(user_id)
        self.get_countries(user_id, legal_entity_id)
        self.get_legal_entities(user_id, client_id, country_id)
        self.get_domains(user_id)
        self.get_unit_location(legal_entity_id)
        self.get_unit_code(legal_entity_id)
        self.get_unit_name(legal_entity_id)
        self.get_statutories(country_id)
        self.get_child_statutories(country_id)
        self.get_statutory_provision(country_id)
        self.get_compliance_task(country_id)
        self.get_compliance_description(country_id)
        self.get_organisation(country_id)
        self.get_applicable_status()

    def get_client_groups(self, user_id):
        data = self._source_db.call_proc("sp_bu_as_user_groups", [user_id])
        for d in data:
            self._client_group_[d["group_name"]] = d

    def get_countries(self, user_id, legal_entity_id):
        data = self._source_db.call_proc("sp_bu_as_user_countries", [
                user_id, legal_entity_id
            ]
        )
        for d in data:
            self._country_[d["country_name"]] = d

    def get_legal_entities(self, user_id, client_id, country_id):
        data = self._source_db.call_proc(
            "sp_bu_as_user_legal_entities", [user_id, client_id, country_id]
        )
        for d in data:
            self._legal_entity_[d["legal_entity_name"]] = d

    def get_domains(self, user_id):
        data = self._source_db.call_proc(
            "sp_bu_as_user_domains", [user_id]
        )
        for d in data:
            self._domain[d["domain_name"]] = d

    def get_unit_location(self, legal_entity_id):
        data = self._source_db.call_proc(
            "sp_bu_unit_location", [legal_entity_id]
        )
        for d in data:
            self._unit_location[d["unit_code"]+'-'+d["geography_name"]] = d

    def get_unit_code(self, legal_entity_id):
        data = self._source_db.call_proc(
            "sp_bu_unit_code_and_name", [legal_entity_id]
        )
        for d in data:
            self._unit_code[d["unit_code"]] = d

    def get_unit_name(self, legal_entity_id):
        data = self._source_db.call_proc(
            "sp_bu_unit_code_and_name", [legal_entity_id]
        )
        for d in data:
            self._unit_name[d["unit_name"]] = d

    def get_statutories(self, country_id):
        data = self._source_db.call_proc(
            "sp_bu_level_one_statutories", [country_id]
        )
        for d in data:
            self._statutories[d["statutory_name"]+'-'+d["domain_name"]] = d

    def get_child_statutories(self, country_id):
        data = self._source_db.call_proc(
            "sp_bu_chils_level_statutories", [country_id]
        )
        for d in data:
            self._child_statutories[
                d["statutory_name"]+'-'+d["parent_name"]+'-'+d["domain_name"]
            ] = d

    def get_statutory_provision(self, country_id):
        data = self._source_db.call_proc("sp_bu_compliance_info", [country_id])
        for d in data:
            self._statutory_provision[d["statutory_provision"]] = d

    def get_compliance_task(self, country_id):
        data = self._source_db.call_proc("sp_bu_compliance_info", [country_id])
        for d in data:
            self._compliance_task[d["compliance_task"]] = d

    def get_compliance_description(self, country_id):
        data = self._source_db.call_proc("sp_bu_compliance_info", [country_id])
        for d in data:
            self._compliance_description[d["compliance_description"]] = d

    def get_organisation(self, country_id):
        data = self._source_db.call_proc(
            "sp_bu_organization_all", [country_id]
        )
        for d in data:
            self._organisation[d["organisation_name"]+'-'+d["domain_name"]] = d

    def get_applicable_status(self):
        data = [
            {'applicable_status': 'applicable'},
            {'applicable_status': 'not applicable'},
            {'applicable_status': 'do not show'}
        ]
        for d in data:
            self._applicable_status[d["applicable_status"]] = d

    def get_compliance_info(self, country_id, domain_ids_):
        domain_ids = ",".join(str(e) for e in domain_ids_)
        data = self._source_db.call_proc_with_multiresult_set(
            "sp_bu_get_all_compliance_info", [country_id, domain_ids], 2
        )

        def status_list(map_id):
            s_legislation = None
            p_legislation = None
            for s in data[0]:
                if s["statutory_mapping_id"] == map_id:
                    if(
                        s["parent_ids"] == '' or s["parent_ids"] == 0 or
                        s["parent_ids"] == '0,'
                    ):
                        s_legislation = s["statutory_name"]
                        p_legislation = s_legislation
                    else:
                        names = [
                            x.strip() for x in s["parent_names"].split('>>')
                            if x != ''
                        ]
                        p_legislation = names[0]
                        if len(names) > 1:
                            s_legislation = names[1]
                        else:
                            s_legislation = s["statutory_name"]
            return p_legislation, s_legislation

        for d in data[1]:
            p_legislation, s_legislation = status_list(
                d["statutory_mapping_id"]
            )
            if s_legislation == p_legislation:
                s_legislation = ""

            key = "%s-%s-%s-%s-%s-%s-%s" % (
                d["compliance_task"], d["compliance_description"],
                d["statutory_provision"], d["country_id"], d["domain_id"],
                p_legislation, s_legislation
            )
            self._compliance_info[key] = d

    def check_base(self, check_status, store, key_name, status_name):
        data = store.get(key_name)
        if data is None:
            return "Not found"

        if check_status is True:
            if status_name is None:
                if data.get("is_active") == 0:
                    return "Status Inactive"
                if data.get("is_closed") == 1:
                    return "Status Inactive"
                if data.get("is_approved") == 0:
                    return "Status Inactive"
        return True

    def check_client_group(self, group_name):
        return self.check_base(
            True, self._client_group_, group_name, None
        )

    def check_country(self, country_name):
        return self.check_base(
            True, self._country_, country_name, None
        )

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(
            True, self._legal_entity_, legal_entity_name, None
        )

    def check_domain(self, domain_name):
        return self.check_base(True, self._domain, domain_name, None)

    def check_unit_location(self, geography_name):
        return self.check_base(True, self._unit_location, geography_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(True, self._unit_code, unit_code, None)

    def check_unit_name(self, unit_name):
        return self.check_base(True, self._unit_name, unit_name, None)

    def check_statutories(self, statutories):
        return self.check_base(False, self._statutories, statutories, None)

    def check_statutory_provision(self, statutory_provision):
        return self.check_base(
            False, self._statutory_provision, statutory_provision, None
        )

    def check_compliance_task(self, compliance_task):
        return self.check_base(
            True, self._compliance_task, compliance_task, None
        )

    def check_compliance_description(self, compliance_description):
        return self.check_base(
            False, self._compliance_description, compliance_description, None
        )

    def check_organisation(self, organisation_name):
        return self.check_base(
            True, self._organisation, organisation_name, None
        )

    def check_applicable_status(self, applicable_status):
        return self.check_base(
            False, self._applicable_status, applicable_status.lower(), None
        )

    def check_child_statutories(self, child_statutories):
        return self.check_base(
            False, self._child_statutories, child_statutories, None
        )

    # save client statutories data in tbl_client_statutories main db
    def save_client_statutories_data(
        self, cl_id, u_id, d_id, user_id, is_rejected, rej_reason
    ):
        created_on = get_date_time()
        status = 3
        if is_rejected is True:
            status = 4

        client_statutory_value = [
            int(cl_id), int(u_id),
            int(d_id), status, rej_reason,
            int(user_id), str(created_on)
        ]
        q = "INSERT INTO tbl_client_statutories (client_id, unit_id, " + \
            " domain_id, status, reason, approved_by, approved_on) values " + \
            " (%s, %s, %s, %s, %s, %s, %s)"
        client_statutory_id = self._source_db.execute_insert(
            q, client_statutory_value
        )

        if client_statutory_id is False:
            raise process_error("E018")
        return client_statutory_id

    # check rejected compliance is available or not in child table
    def get_client_compliance_rejected_status(
        self, legal_entity, domain, unit_code, csv_id
    ):
        res = self._db.call_proc(
            "sp_check_client_compliance_rejected_status",
            [
                legal_entity, domain, unit_code, csv_id
            ]
        )
        if len(res) > 0:
            return True, res[0]["remarks"]
        else:
            return False, None

    # save client compliance data in tbl_client_compliances main db
    def save_client_compliances_data(
        self, cl_id, le_id, u_id, d_id, cs_id, data, user_id, country_id_,
        is_rejected, saved_by, saved_on
    ):
        created_on = get_date_time()
        columns = [
            "client_statutory_id",
            "client_id", "legal_entity_id", "unit_id",
            "domain_id", "statutory_id", "statutory_applicable_status",
            "remarks", "compliance_id", "compliance_applicable_status",
            "is_saved", "saved_by", "saved_on", "is_submitted", "submitted_by",
            "submitted_on", "is_approved", "approved_by", "approved_on",
            "updated_by", "updated_on"
        ]

        values = []
        for idx, d in enumerate(data):
            approval_status = 0
            submitted_status = 0

            if is_rejected is True and d["action"] == 1:
                approval_status = 2
            elif d["Compliance_Applicable_Status"] == 3 and d["action"] == 1:
                approval_status = 3
            elif d["Compliance_Applicable_Status"] != 3 and d["action"] == 1:
                approval_status = 99
                submitted_status = 1
            else:
                approval_status = 4

            p_legislation_id = self._statutories.get(
                d["Primary_Legislation"]+'-'+d["Domain"]).get(
                "statutory_id"
            )

            key = "%s-%s-%s-%s-%s-%s-%s" % (
                d["Compliance_Task"], d["Compliance_Description"],
                d["Statutory_Provision"], country_id_, d_id,
                d["Primary_Legislation"], d["Secondary_Legislation"]
            )
            comp_id = self._compliance_info.get(key).get(
                "compliance_id"
            )

            values.append((
                int(cs_id), cl_id, le_id, u_id, d_id, p_legislation_id,
                d["Statutory_Applicable_Status"],
                d["Statutory_remarks"], comp_id,
                d["Compliance_Applicable_Status"],
                1, saved_by, saved_on,
                submitted_status, saved_by, saved_on,
                approval_status, int(user_id), created_on,
                int(user_id), created_on
            ))

        if values:
            self._source_db.bulk_insert(
                "tbl_client_compliances", columns, values
            )

            q = "update tbl_client_compliances set is_approved = 5 " + \
                "where is_approved = 99 and client_statutory_id = %s"
            params = [int(cs_id)]
            self._source_db.execute(q, params)
            return True
        else:
            return False

    # main db related validation mapped with field name
    def statusCheckMethods(self):
        self._validation_maps = {
            "Client_Group": self.check_client_group,
            "Country": self.check_country,
            "Legal_Entity": self.check_legal_entity,
            "Domain": self.check_domain,
            "Unit_Location": self.check_unit_location,
            "Unit_Code": self.check_unit_code,
            "Unit_Name": self.check_unit_name,
            "Primary_Legislation": self.check_statutories,
            "Secondary_Legislation": self.check_child_statutories,
            "Statutory_Provision": self.check_statutory_provision,
            "Compliance_Task": self.check_compliance_task,
            "Compliance_Description": self.check_compliance_description,
            "Organization": self.check_organisation,
            "Statutory_Applicable_Status": self.check_applicable_status,
            "Compliance_Applicable_Status": self.check_applicable_status
        }

    # declare csv column field name
    def csv_column_fields(self):
        self._csv_column_name = [
            "S.No", "Client_Group", "Country", "Legal_Entity", "Domain",
            "Organization", "Unit_Code", "Unit_Name",
            "Unit_Location", "Primary_Legislation", "Secondary_Legislation",
            "Statutory_Provision", "Compliance_Task",
            "Compliance_Description", "Statutory_Applicable_Status",
            "Statutory_remarks", "Compliance_Applicable_Status"
        ]

    def get_all_assigned_compliance_knowledge(
        self, client_id, legal_entity_id
    ):
        domain_ids = ",".join(str(e) for e in self._domain_ids)
        unit_ids = ",".join(str(e) for e in self._unit_ids)
        data = self._source_db.call_proc(
            'sp_bu_get_assigned_compliances_for_unit',
            [
                client_id, legal_entity_id,
                domain_ids, unit_ids
            ]
        )
        data_str = ""
        for d in data:
            data_str = str(d["domain_id"])
            data_str += "-" + str(d["unit_id"])
            data_str += "-" + str(d["compliance_id"])
            self._assigned_compliances_knowledge.append(data_str)

    # check duplicate compliance in already existing knowledge table
    def check_compliance_task_name_duplicate_in_knowledge(
        self, data, country_id
    ):
        domain_name = data.get("Domain")
        domain_id = self._domain.get(domain_name).get("domain_id")
        unit_code = data.get("Unit_Code")
        unit_id = self._unit_code.get(unit_code).get("unit_id")

        key = "%s-%s-%s-%s-%s-%s-%s" % (
            data.get("Compliance_Task"), data.get("Compliance_Description"),
            data.get("Statutory_Provision"), country_id, domain_id,
            data.get("Primary_Legislation"), data.get("Secondary_Legislation")
        )
        comp_id = self._compliance_info.get(key).get(
            "compliance_id"
        )

        compare_str = str(domain_id)
        compare_str += "-" + str(unit_id)
        compare_str += "-" + str(comp_id)

        if len(self._assigned_compliances_knowledge) > 0:
            if compare_str in self._assigned_compliances_knowledge:
                return False
            else:
                return True
        return True

    # save domain executive notification message
    def save_executive_message(
        self, a_type, csv_name, clientgroup, legalentity, createdby, unitids,
        reason, declined_count
    ):
        admin_users_id = []
        res = self._source_db.call_proc("sp_users_under_user_category", (1,))
        for user in res:
            admin_users_id.append(user["user_id"])

        domain_users_id = []
        res = self._source_db.call_proc("sp_bu_user_by_unit_ids", (8, unitids))
        for user in res:
            domain_users_id.append(user["user_id"])

        if a_type == 1:
            action_type = "approved"
        else:
            action_type = "rejected with following reason %s" % (reason)

        if declined_count > 0:
            action_type = "declined"
            declined_text = "%s records" % (declined_count)
            msg = "Assign statutory file %s of %s - %s %s has been %s" % (
                csv_name, clientgroup, legalentity, declined_text, action_type
            )
        else:
            msg = "Assign statutory file %s of %s - %s has been %s" % (
                csv_name, clientgroup, legalentity, action_type
            )

        if len(domain_users_id) > 0:
            self._source_db.save_toast_messages(
                8, "Approve Assign Statutory Bulk Upload", msg, None,
                domain_users_id, createdby
            )
        if len(admin_users_id) > 0:
            self._source_db.save_toast_messages(
                1, "Approve Assign Statutory Bulk Upload", msg, None,
                admin_users_id, createdby
            )
        self._source_db.save_activity(
            createdby, frmApproveAssignStatutoryBulkUpload, msg
        )

    # save domain manager notification message
    def save_manager_message(
        self, csv_name, domainname, unitname, createdby, unitids
    ):
        admin_users_id = []
        res = self._source_db.call_proc("sp_users_under_user_category", (1,))
        for user in res:
            admin_users_id.append(user["user_id"])

        domain_users_id = []
        res = self._source_db.call_proc("sp_bu_user_by_unit_ids", (7, unitids))
        for user in res:
            domain_users_id.append(user["user_id"])

        msg = "Assign statutory file %s of %s - %s uploaded for your %s " % (
            csv_name, unitname, domainname, 'approval'
        )

        if len(domain_users_id) > 0:
            self._source_db.save_toast_messages(
                7, "Assign Statutory Bulk Upload", msg, None, domain_users_id,
                createdby
            )
        if len(admin_users_id) > 0:
            self._source_db.save_toast_messages(
                1, "Assign Statutory Bulk Upload", msg, None, admin_users_id,
                createdby
            )
        self._source_db.save_activity(
            createdby, frmAssignStatutoryBulkUpload, msg
        )

    # get country_id and legal_entity_id by legal_entity_name
    def get_init_info(self):
        client_id = 0
        country_id = 0
        legal_entity_id = 0

        for k, v in groupby(self._source_data, key=lambda s: (
            s["Client_Group"], s["Country"], s["Legal_Entity"]
        )):
            grouped_list = list(v)
            group_name = grouped_list[0].get("Client_Group")
            country_name = grouped_list[0].get("Country")
            legal_entity_name = grouped_list[0].get("Legal_Entity")

            group_result = self._source_db.call_proc(
                "sp_bu_get_group_id_by_name", [group_name]
            )
            if len(group_result) > 0:
                client_id = group_result[0]["client_id"]

            country_result = self._source_db.call_proc(
                "sp_bu_get_country_id_by_name", [country_name]
            )
            if len(country_result) > 0:
                country_id = country_result[0]["country_id"]

            le_result = self._source_db.call_proc(
                "sp_bu_get_legal_entity_id_by_name",
                [
                    client_id, country_id, legal_entity_name
                ]
            )
            if len(le_result) > 0:
                legal_entity_id = le_result[0]["legal_entity_id"]

        return client_id, country_id, legal_entity_id

    # commit database after execute query
    def source_commit(self):
        self._source_db.commit()


class ValidateAssignStatutoryCsvData(SourceDB):
    def __init__(
        self, db, source_data, session_user, csv_name, csv_header
    ):
        SourceDB.__init__(self)
        self._db = db
        self._source_data = source_data
        self._session_user_obj = session_user
        self._csv_name = csv_name
        self._csv_header = csv_header
        self._error_summary = {}
        self.error_summary()
        self._client_id = None
        self._client_group = None
        self._unit_ids = []
        self._unit_codes = []
        self._legal_entity_id = None
        self._legal_entity = None
        self._domain_ids = []
        self._domain_names = []
        self._country = None
        self._sheet_name = "Assign Statutory"

        self._compliances_downloaded = []
        self._compliances_uploaded = []

    def connect_bulk_database(self):
        c_db_con = bulkupload_db_connect()
        self._db = Database(c_db_con)
        self._db.begin()

    # error summary mapped with initial count
    def error_summary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error": 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0
        }

    # compare declared csv column with uploaded csv column heading
    def compare_csv_columns(self):
        res = collections.Counter(
            self._csv_column_name) == collections.Counter(self._csv_header)
        return res
    '''
        looped csv data to perform corresponding validation
        returns: valid and invalid return format
        rType: dictionary
    '''

    # check deplicate row in uploaded csv file
    def check_duplicate_in_csv(self):
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Duplicate data found in CSV")

    # check duplicate compliance for same unit in csv file
    def check_duplicate_compliance_for_same_unit_in_csv(self):
        duplicate_compliance = 0
        duplicate_compliance_row = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"], s["Unit_Code"], s["Statutory_Provision"],
            s["Compliance_Task"], s["Compliance_Description"],
            s["Primary_Legislation"], s["Secondary_Legislation"],
            s["Legal_Entity"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                duplicate_compliance += len(grouped_list)
                duplicate_compliance_row.append([
                    grouped_list[0].get("Statutory_Provision"),
                    grouped_list[0].get("Compliance_Task"),
                    grouped_list[0].get("Compliance_Description"),
                ])
        return duplicate_compliance, duplicate_compliance_row

    # check uploaded and downloaded compliance count for unit in csv file
    def check_uploaded_count_in_csv(self):
        unit_names = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Legal_Entity"], s["Domain"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) >= 1:
                unit_code = grouped_list[0].get("Unit_Code")
                domain = grouped_list[0].get("Domain")
                legal_entity = grouped_list[0].get("Legal_Entity")
                country = grouped_list[0].get("Country")
                client_group = grouped_list[0].get("Client_Group")
                data = self._db.call_proc(
                    "sp_check_upload_compliance_count_for_unit",
                    [client_group, country, legal_entity, domain, unit_code]
                )
                uploaded_count = data[0]["count"]

                if(len(grouped_list) != uploaded_count):
                    unit_names.append(grouped_list[0].get("Unit_Code"))
        return unit_names

    # get master table related values while upload csv
    def get_master_table_info(self):
        self._domain_names = []
        self._domain_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"]
        )):
            grouped_list = list(v)
            if len(grouped_list) >= 1:
                self._domain_names.append(grouped_list[0].get("Domain"))

                if(
                    self._domain.get(grouped_list[0].get("Domain"))
                ) is not None:
                    self._domain_ids.append(self._domain.get(
                        grouped_list[0].get("Domain")).get("domain_id")
                    )

                self._legal_entity = grouped_list[0].get("Legal_Entity")
                self._country = grouped_list[0].get("Country")

                if(
                    self._legal_entity_.get(
                        grouped_list[0].get("Legal_Entity")
                    )
                ) is not None:
                    self._legal_entity_id = self._legal_entity_.get(
                        grouped_list[0].get("Legal_Entity")
                    ).get("legal_entity_id")

                self._client_group = grouped_list[0].get("Client_Group")

                if(
                    self._client_group_.get(
                        grouped_list[0].get("Client_Group")
                    )
                ) is not None:
                    self._client_id = self._client_group_.get(
                        grouped_list[0].get("Client_Group")
                    ).get("client_id")

        self._unit_ids = []
        self._unit_codes = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) >= 1:
                self._unit_codes.append(grouped_list[0].get("Unit_Code"))
                if(
                    self._unit_code.get(grouped_list[0].get("Unit_Code"))
                ) is not None:
                    self._unit_ids.append(self._unit_code.get(
                        grouped_list[0].get("Unit_Code")).get("unit_id")
                    )
        self._unit_ids = list(set(self._unit_ids))

    # check invalid compliance in csv while upload
    def check_invalid_compliance_in_csv(self, data):
        compare_str = str(data.get("Client_Group"))
        compare_str += "-" + str(data.get("Country"))
        compare_str += "-" + str(data.get("Legal_Entity"))
        compare_str += "-" + str(data.get("Domain"))
        compare_str += "-" + str(data.get("Organization").replace(
            CSV_DELIMITER, ","))
        compare_str += "-" + str(data.get("Unit_Code"))
        compare_str += "-" + str(data.get("Unit_Name"))
        compare_str += "-" + str(data.get("Unit_Location"))
        compare_str += "-" + str(data.get("Primary_Legislation"))
        compare_str += "-" + str(data.get("Secondary_Legislation"))
        compare_str += "-" + str(data.get("Statutory_Provision"))
        compare_str += "-" + str(data.get("Compliance_Task"))
        compare_str += "-" + str(data.get("Compliance_Description"))

        if len(self._compliances_downloaded) > 0:
            if compare_str in self._compliances_downloaded:
                return True
            else:
                return False
        return False

    # check duplicate compliance for same unit in temp db
    def check_compliance_task_name_duplicate(
        self, data
    ):
        compare_str = str(data.get("Legal_Entity"))
        compare_str += "-" + str(data.get("Domain"))
        compare_str += "-" + str(data.get("Unit_Code"))
        compare_str += "-" + str(data.get("Primary_Legislation"))
        compare_str += "-" + str(data.get("Secondary_Legislation"))
        compare_str += "-" + str(data.get("Statutory_Provision"))
        compare_str += "-" + str(data.get("Compliance_Task"))
        compare_str += "-" + str(data.get("Compliance_Description"))

        if len(self._compliances_uploaded) > 0:
            if compare_str in self._compliances_uploaded:
                return False
            else:
                return True
        return True

    def get_all_downloaded_compliances(self):
        domain_names = ",".join(str(e) for e in self._domain_names)
        unit_codes = ",".join(str(e) for e in self._unit_codes)
        data = self._db.call_proc(
            'sp_get_all_downloaded_compliances',
            [
                self._client_group, self._country, self._legal_entity,
                domain_names, unit_codes
            ]
        )
        data_str = ""
        for d in data:
            data_str = str(d["client_group"])
            data_str += "-" + str(d["country"])
            data_str += "-" + str(d["legal_entity"])
            data_str += "-" + str(d["domain"])
            data_str += "-" + str(d["organization"])
            data_str += "-" + str(d["unit_code"])
            data_str += "-" + str(d["unit_name"])
            data_str += "-" + str(d["unit_location"])
            data_str += "-" + str(d["perimary_legislation"])
            data_str += "-" + str(d["secondary_legislation"])
            data_str += "-" + str(d["statutory_provision"])
            data_str += "-" + str(d["compliance_task_name"])
            data_str += "-" + str(d["compliance_description"])
            self._compliances_downloaded.append(data_str)

    def get_all_uploaded_compliances(self):
        domain_names = ",".join(str(e) for e in self._domain_names)
        unit_codes = ",".join(str(e) for e in self._unit_codes)
        data = self._db.call_proc(
            'sp_get_all_uploaded_compliances',
            [
                self._client_group, self._legal_entity,
                domain_names, unit_codes
            ]
        )
        data_str = ""
        for d in data:
            data_str = str(d["legal_entity"])
            data_str += "-" + str(d["domain"])
            data_str += "-" + str(d["unit_code"])
            data_str += "-" + str(d["perimary_legislation"])
            data_str += "-" + str(d["secondary_legislation"])
            data_str += "-" + str(d["statutory_provision"])
            data_str += "-" + str(d["compliance_task_name"])
            data_str += "-" + str(d["compliance_description"])
            self._compliances_uploaded.append(data_str)

    def make_error_desc(self, res, msg):
            if res is True:
                res = []
            if res is not True:
                if type(msg) is list:
                    res.extend(msg)
                else:
                    res.append(msg)
            return res

    # check uploaded csv validation process

    def check_validation(
        self, res, row_idx, data, duplicate_compliance_row, error_count,
        mapped_header_dict
    ):
        for key in self._csv_column_name:
            value = data.get(key)
            isFound = ""
            values = value.strip().split(CSV_DELIMITER)
            csvParam = csv_params_as.get(key)
            for v in [v.strip() for v in values]:
                if (
                    key == 'Statutory_remarks' and
                    (
                        (
                            data.get(
                                'Statutory_Applicable_Status'
                            ).lower() == 'not applicable' or
                            data.get(
                                'Statutory_Applicable_Status'
                            ).lower() == 'do not show'
                        ) and
                        data.get('Statutory_remarks') == ''
                    )
                ):
                    self._error_summary["mandatory_error"] += 1
                    mandatory_error = "Statutory_remarks - Field is blank"
                    res = self.make_error_desc(res, mandatory_error)

                if (
                    key == 'Statutory_remarks' and
                    (
                        data.get(
                            'Statutory_Applicable_Status'
                        ).lower() == 'applicable' and
                        data.get('Statutory_remarks') != ''
                    )
                ):
                    self._error_summary["mandatory_error"] += 1
                    mandatory_error = "Statutory_Remarks - Not Required"
                    res = self.make_error_desc(res, mandatory_error)
                valid_failed, error_cnt = parse_csv_dictionary_values_as(
                    key, v
                )
                if valid_failed is not True:
                    if res is True:
                        res = valid_failed
                        error_count = error_cnt
                    else:
                        res.extend(valid_failed)
                        error_count["mandatory"] += error_cnt["mandatory"]
                        error_count["max_length"] += error_cnt["max_length"]
                        error_count["invalid_char"] += error_cnt[
                            "invalid_char"
                        ]
                if v != "":
                    if (
                        csvParam.get("check_is_exists") is True or
                        csvParam.get("check_is_active") is True
                    ):
                        unboundMethod = self._validation_maps.get(key)
                        if unboundMethod is not None:
                            if(
                                key == "Organization" or
                                key == "Primary_Legislation"
                            ):
                                org_val = v+'-'+data.get('Domain')
                                isFound = unboundMethod(org_val)
                            elif key == "Secondary_Legislation":
                                s_legs_val = v+'-'+data.get("Primary_Legislation")+'-'+data.get('Domain')
                                isFound = unboundMethod(s_legs_val)
                            elif key == "Unit_Location":
                                loc_val = data.get('Unit_Code')+'-'+v
                                isFound = unboundMethod(loc_val)
                            else:
                                isFound = unboundMethod(v)
                        if isFound is not True and isFound != "":
                            if key == "Organization":
                                msg = "%s - %s %s" % (key, v, isFound)
                            else:
                                msg = "%s - %s" % (key, isFound)
                            if res is not True:
                                res.append(msg)
                            else:
                                res = [msg]
                            if "Status" in isFound:
                                self._error_summary["inactive_error"] += 1
                            else:
                                self._error_summary["invalid_data_error"] += 1
            if res is not True:
                err_str = (',').join(res)
                if err_str.find(key) != -1:
                    head_idx = mapped_header_dict.get(key)
                    if head_idx is None:
                        head_idx = [row_idx]
                    else:
                        head_idx.append(row_idx)
                    mapped_header_dict[key] = head_idx
            if key == "Compliance_Task":
                for x in duplicate_compliance_row:
                    if (
                        x[0] == data.get("Statutory_Provision") and
                        x[1] == data.get("Compliance_Task") and
                        x[2] == data.get("Compliance_Description")
                    ):
                        dup_error = "Duplicate Compliance"
                        res = self.make_error_desc(res, dup_error)
        return res, mapped_header_dict, error_count

    # call perform validation function
    def perform_validation(self):
        self.connect_bulk_database()
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        if(self.compare_csv_columns() is False):
            return "InvalidCSV"

        duplicate = self.check_duplicate_compliance_for_same_unit_in_csv()
        duplicate_compliance_in_csv = duplicate[0]
        duplicate_compliance_row = duplicate[1]
        self._error_summary["duplicate_error"] += duplicate_compliance_in_csv
        client_id, country_id, legal_entity_id = self.get_init_info()

        self.init_values(
            self._session_user_obj.user_id(), client_id, country_id,
            legal_entity_id
        )
        is_get_master_info = False

        for row_idx, data in enumerate(self._source_data):
            res, mapped_header_dict, error_count = self.check_validation(
                True,
                row_idx,
                data,
                duplicate_compliance_row,
                {"mandatory": 0, "max_length": 0, "invalid_char": 0},
                mapped_header_dict
            )
            if res is True:
                if is_get_master_info is False:
                    self.get_master_table_info()
                    self.get_all_downloaded_compliances()
                    self.get_all_uploaded_compliances()
                    self.get_all_assigned_compliance_knowledge(
                        client_id, legal_entity_id
                    )
                    self.get_compliance_info(country_id, self._domain_ids)
                    is_get_master_info = True

                # changed
                if not self.check_invalid_compliance_in_csv(
                    data
                ):
                    self._error_summary["invalid_data_error"] += 1
                    invalid_error = "Invalid Compliance"
                    res = self.make_error_desc(res, invalid_error)

                # changed
                if not self.check_compliance_task_name_duplicate(data):
                    self._error_summary["duplicate_error"] += 1
                    dup_error = "Duplicate Compliance in Temp DB"
                    res = self.make_error_desc(res, dup_error)

                # changed
                if not self.check_compliance_task_name_duplicate_in_knowledge(
                    data, country_id
                ):
                    self._error_summary["duplicate_error"] += 1
                    dup_error = "Duplicate Compliance"
                    res = self.make_error_desc(res, dup_error)

            if res is not True:
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else:
                    error_list.extend(res)
                res = True
                mapped_error_dict[row_idx] = error_list
                invalid += 1
                self._error_summary["mandatory_error"] += error_count[
                    "mandatory"
                ]
                self._error_summary["max_length_error"] += error_count[
                    "max_length"
                ]
                self._error_summary["invalid_char_error"] += error_count[
                    "invalid_char"
                ]

        if invalid > 0:
            return self.make_invalid_return(
                mapped_error_dict, mapped_header_dict
            )
        else:
            return self.make_valid_return(
                mapped_error_dict, mapped_header_dict
            )

    # frame invalid return function while upload csv
    def make_invalid_return(self, mapped_error_dict, mapped_header_dict):
        fileString = self._csv_name.split('.')
        file_name = "%s_%s.%s" % (
            fileString[0], "invalid", "xlsx"
        )
        final_hearder = self._csv_header
        final_hearder.append("Error Description")
        write_data_to_excel(
            os.path.join(BULKUPLOAD_INVALID_PATH, "xlsx"), file_name,
            final_hearder, self._source_data, mapped_error_dict,
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
            "invalid_char_error": self._error_summary["invalid_char_error"],
            "invalid_data_error": self._error_summary["invalid_data_error"],
            "inactive_error": self._error_summary["inactive_error"],
            "total": total,
            "invalid": invalid
        }

    # frame valid return function while upload csv
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
        self._declined_row_idx = {}
        self.get_source_data()
        self._legal_entity = None
        self._client_group = None
        self._csv_name = None
        self._unit_ids = None
        self._domain_ids = None

    def connect_bulk_database(self):
        c_db_con = bulkupload_db_connect()
        self._db = Database(c_db_con)
        self._db.begin()

    def source_bulkdb_commit(self):
        self._db.commit()

    # get uploaded details by csv_id for approval process
    def get_source_data(self):
        self.connect_bulk_database()
        self._source_data = self._db.call_proc(
            "sp_assign_statutory_by_csvid", [self._csv_id]
        )

    # perform validate records before submit record to main db
    def perform_validation_before_submit(self):
        declined_count = 0
        self._declined_row_idx = {}
        country_id, country_name = get_country_name_by_legal_entity_id(
            self._legal_entity_id
        )
        self.init_values(
            self._session_user_obj.user_id(), self._client_id, country_id,
            self._legal_entity_id
        )

        self._unit_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) >= 1:
                if(
                    self._unit_code.get(grouped_list[0].get("Unit_Code"))
                ) is not None:
                    self._unit_ids.append(self._unit_code.get(
                        grouped_list[0].get("Unit_Code")).get("unit_id")
                    )
        self._unit_ids = list(set(self._unit_ids))

        self._domain_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"]
        )):
            grouped_list = list(v)
            if len(grouped_list) >= 1:
                if(
                    self._domain.get(grouped_list[0].get("Domain"))
                ) is not None:
                    self._domain_ids.append(self._domain.get(
                        grouped_list[0].get("Domain")).get("domain_id")
                    )

        is_get_master_info = False

        for row_idx, data in enumerate(self._source_data):
            res = True
            declined_count = 0
            if row_idx == 0:
                self._legal_entity = data.get("Legal_Entity")
                self._client_group = data.get("Client_Group")
                self._csv_name = data.get("Csv_Name")

            for key in self._csv_column_name:
                value = data.get(key)
                isFound = ""
                if value is None:
                    continue

                csvParam = csv_params_as.get(key)
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
                                unboundMethod = self._validation_maps.get(
                                    key
                                )
                                if(
                                    key == "Organization" or
                                    key == "Primary_Legislation"
                                ):
                                    org_val = v+'-'+data.get('Domain')
                                    isFound = unboundMethod(org_val)
                                elif key == "Secondary_Legislation":
                                    s_legs_val = v+'-'+data.get(
                                        'Primary_Legislation'
                                        )+'-'+data.get('Domain')
                                    isFound = unboundMethod(s_legs_val)
                                elif key == "Unit_Location":
                                    loc_val = data.get('Unit_Code')+'-'+v
                                    isFound = unboundMethod(loc_val)
                                else:
                                    isFound = unboundMethod(v)

                            if isFound is not True and isFound != "":
                                declined_count += 1
                                if key == "Organization":
                                    msg = "%s - %s %s" % (key, v, isFound)
                                else:
                                    msg = "%s - %s" % (key, isFound)

                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]

            if is_get_master_info is False:
                self.get_all_assigned_compliance_knowledge(
                    self._client_id, self._legal_entity_id
                )
                self.get_compliance_info(country_id, self._domain_ids)
                is_get_master_info = True

            if not self.check_compliance_task_name_duplicate_in_knowledge(
                data, country_id
            ):
                declined_count += 1
                dup_error = "Compliance_Task - Duplicate data"
                if res is not True:
                    res.append(dup_error)
                else:
                    res = [dup_error]

            if declined_count > 0:
                self._declined_row_idx[
                    data.get("bulk_assign_statutory_id")
                ] = res

        return self._declined_row_idx

    # frame record for main db while approval process
    def frame_data_for_main_db_insert(self, user_id):
        self.get_source_data()
        self._source_data.sort(key=lambda x: (
            x["Domain"], x["Unit_Code"]
        ))
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) == 0:
                continue

            unit_id = None
            domain_id = None
            value = grouped_list[0]

            unit_id = self._unit_code.get(
                value.get("Unit_Code")
            ).get("unit_id")
            domain_id = self._domain.get(value.get("Domain")).get("domain_id")

            country_id, country_name = get_country_name_by_legal_entity_id(
                self._legal_entity_id
            )

            is_rejected, reason = self.get_client_compliance_rejected_status(
                value.get("Legal_Entity"), value.get("Domain"),
                value.get("Unit_Code"), self._csv_id
            )

            cs_id = self.save_client_statutories_data(
                self._client_id, unit_id, domain_id, user_id, is_rejected,
                reason
            )

            self.save_client_compliances_data(
                self._client_id, self._legal_entity_id, unit_id, domain_id,
                cs_id, grouped_list, user_id, country_id, is_rejected,
                value.get("uploaded_by"), value.get("uploaded_on")
            )

    # frame data for system rejected information while approval process
    def make_rejection(self, declined_info, user_id):
        try:
            self._db = connect_bulk_db()
            created_on = get_date_time()
            count = len(declined_info.keys())
            for k, v in declined_info.items():
                remarks = ",".join(v)
                q = "update tbl_bulk_assign_statutory set " + \
                    "action = 3, remarks = %s where " + \
                    "bulk_assign_statutory_id = %s"
                self._db.execute(q, [
                    remarks, k
                ])

            q1 = "update tbl_bulk_assign_statutory_csv set " + \
                " declined_count = %s, approve_status = 1, " + \
                " approved_by = %s, approved_on = %s, " + \
                " total_rejected_records = (select count(0) from " + \
                " tbl_bulk_assign_statutory as t WHERE t.action = 2 and " + \
                " t.csv_assign_statutory_id = %s) WHERE " + \
                " csv_assign_statutory_id = %s"

            self._db.execute(q1, [
                count, user_id, created_on, self._csv_id, self._csv_id
            ])
            self._db.commit()

        except Exception, e:
            raise (e)

    def update_child(self, csv_id):
        try:
            q = "update tbl_bulk_assign_statutory set " + \
                " action = 1 where " + \
                " csv_assign_statutory_id = %s "
            self._db.execute(q, [csv_id])

        except Exception, e:
            raise (e)


def bulkupload_db_connect():
    cnx_pool = mysql.connector.connect(
        user=BULK_UPLOAD_DB_USERNAME,
        password=BULK_UPLOAD_DB_PASSWORD,
        host=BULK_UPLOAD_DB_HOST,
        database=BULK_UPLOAD_DATABASE_NAME,
        port=BULK_UPLOAD_DB_PORT,
        autocommit=False,
    )
    return cnx_pool


def connect_bulk_db():
    _bulk_db = None
    try:
        _bulk_db_con = mysql.connector.connect(
            user=BULK_UPLOAD_DB_USERNAME,
            password=BULK_UPLOAD_DB_PASSWORD,
            host=BULK_UPLOAD_DB_HOST,
            database=BULK_UPLOAD_DATABASE_NAME,
            port=BULK_UPLOAD_DB_PORT,
            autocommit=False
        )
        _bulk_db = Database(_bulk_db_con)
        _bulk_db.begin()
    except Exception, e:
        print "Connection Exception Caught"
        print e
    return _bulk_db
