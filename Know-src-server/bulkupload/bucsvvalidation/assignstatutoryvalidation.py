
import os
import collections
import mysql.connector
from server.exceptionmessage import process_error
from itertools import groupby
from server.dbase import Database
from server.constants import (
    KNOWLEDGE_DB_HOST, KNOWLEDGE_DB_PORT, KNOWLEDGE_DB_USERNAME,
    KNOWLEDGE_DB_PASSWORD, KNOWLEDGE_DATABASE_NAME,
    CSV_DELIMITER, BULKUPLOAD_INVALID_PATH

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
        self.Client_Group = {}
        self.Legal_Entity = {}
        self.Domain = {}
        self.Unit_Location = {}
        self.Unit_Code = {}
        self.Unit_Name = {}
        self.Statutories = {}
        self.Child_Statutories = {}
        self.Statutory_Provision = {}
        self.Compliance_Task = {}
        self.Compliance_Description = {}
        self.Organisation = {}
        self.Applicable_Status = {}
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

    def init_values(self, user_id):
        self.get_client_groups(user_id)
        self.get_legal_entities(user_id)
        self.get_domains(user_id)
        self.get_unit_location()
        self.get_unit_code()
        self.get_unit_name()
        self.get_statutories()
        self.get_child_statutories()
        self.get_statutory_provision()
        self.get_compliance_task()
        self.get_compliance_description()
        self.get_organisation()
        self.get_applicable_status()

    def get_client_groups(self, user_id):
        data = self._source_db.call_proc("sp_bu_as_user_groups", [user_id])
        for d in data:
            self.Client_Group[d["group_name"]] = d

    def get_legal_entities(self, user_id):
        data = self._source_db.call_proc(
            "sp_bu_as_user_legal_entities", [user_id]
        )
        for d in data:
            self.Legal_Entity[d["legal_entity_name"]] = d

    def get_domains(self, user_id):
        data = self._source_db.call_proc(
            "sp_bu_as_user_domains", [user_id]
        )
        for d in data:
            self.Domain[d["domain_name"]] = d

    def get_unit_location(self):
        data = self._source_db.call_proc("sp_bu_client_unit_geographies")
        for d in data:
            self.Unit_Location[d["geography_name"]] = d

    def get_unit_code(self):
        data = self._source_db.call_proc(
            "sp_bu_unit_code_and_name"
        )
        for d in data:
            self.Unit_Code[d["unit_code"]] = d

    def get_unit_name(self):
        data = self._source_db.call_proc(
            "sp_bu_unit_code_and_name"
        )
        for d in data:
            self.Unit_Name[d["unit_name"]] = d

    def get_statutories(self):
        data = self._source_db.call_proc("sp_bu_level_one_statutories")
        for d in data:
            self.Statutories[d["statutory_name"]] = d

    def get_child_statutories(self):
        data = self._source_db.call_proc("sp_bu_chils_level_statutories")
        for d in data:
            self.Child_Statutories[d["statutory_name"]] = d

    def get_statutory_provision(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data:
            self.Statutory_Provision[d["statutory_provision"]] = d

    def get_compliance_task(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data:
            self.Compliance_Task[d["compliance_task"]] = d

    def get_compliance_description(self):
        data = self._source_db.call_proc("sp_bu_compliance_info")
        for d in data:
            self.Compliance_Description[d["compliance_description"]] = d

    def get_organisation(self):
        data = self._source_db.call_proc("sp_bu_organization_all")
        for d in data:
            self.Organisation[d["organisation_name"]] = d

    def get_applicable_status(self):
        data = [
            {'applicable_status': 'applicable'},
            {'applicable_status': 'not applicable'},
            {'applicable_status': 'do not show'}
        ]
        for d in data:
            self.Applicable_Status[d["applicable_status"]] = d

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
        return True

    def check_client_group(self, group_name):
        return self.check_base(
            True, self.Client_Group, group_name, None
            )

    def check_legal_entity(self, legal_entity_name):
        return self.check_base(
            True, self.Legal_Entity, legal_entity_name, None
            )

    def check_domain(self, domain_name):
        return self.check_base(True, self.Domain, domain_name, None)

    def check_unit_location(self, geography_name):
        return self.check_base(True, self.Unit_Location, geography_name, None)

    def check_unit_code(self, unit_code):
        return self.check_base(True, self.Unit_Code, unit_code, None)

    def check_unit_name(self, unit_name):
        return self.check_base(True, self.Unit_Name, unit_name, None)

    def check_statutories(self, statutories):
        return self.check_base(False, self.Statutories, statutories, None)

    def check_statutory_provision(self, statutory_provision):
        return self.check_base(
            False, self.Statutory_Provision, statutory_provision, None
            )

    def check_compliance_task(self, compliance_task):
        return self.check_base(
            True, self.Compliance_Task, compliance_task, None
            )

    def check_compliance_description(self, compliance_description):
        return self.check_base(
            False, self.Compliance_Description, compliance_description, None
        )

    def check_organisation(self, organisation_name):
        return self.check_base(
            True, self.Organisation, organisation_name, None
        )

    def check_applicable_status(self, applicable_status):
        return self.check_base(
            False, self.Applicable_Status, applicable_status.lower(), None
        )

    def check_child_statutories(self, child_statutories):
        return self.check_base(
            False, self.Child_Statutories, child_statutories, None
        )

    def save_client_statutories_data(self, cl_id, u_id, d_id, user_id):
        created_on = get_date_time()
        client_statutory_value = [
            int(cl_id), int(u_id),
            int(d_id), 3,
            int(user_id), str(created_on)
        ]
        q = "INSERT INTO tbl_client_statutories (client_id, unit_id, " + \
            " domain_id, status, approved_by, approved_on) values " + \
            " (%s, %s, %s, %s, %s, %s)"
        client_statutory_id = self._source_db.execute_insert(
            q, client_statutory_value
        )

        if client_statutory_id is False:
            raise process_error("E018")
        return client_statutory_id

    def save_client_compliances_data(
        self, cl_id, le_id, u_id, d_id, cs_id, data, user_id
    ):
        created_on = get_date_time()
        columns = [
            "client_statutory_id",
            "client_id", "legal_entity_id", "unit_id",
            "domain_id", "statutory_id", "statutory_applicable_status",
            "remarks", "compliance_id", "compliance_applicable_status",
            "is_submitted", "is_approved", "approved_by", "approved_on",
            "updated_by", "updated_on"
        ]

        values = []
        for idx, d in enumerate(data):
            approval_status = 0
            submitted_status = 0
            if d["Compliance_Applicable_Status"] == 3 and d["action"] == 1:
                approval_status = 3
            elif d["Compliance_Applicable_Status"] != 3 and d["action"] == 1:
                approval_status = 5
                submitted_status = 1
            else:
                approval_status = 4

            statu_id = self.Statutories.get(d["Primary_Legislation"]).get(
                "statutory_id"
                )
            comp_id = None
            c_ids = self._source_db.call_proc(
                "sp_bu_get_compliance_id_by_name",
                [
                    d["Compliance_Task"], d["Compliance_Description"]
                ])
            for c_id in c_ids:
                comp_id = c_id["compliance_id"]

            values.append((
                int(cs_id), cl_id, le_id, u_id, d_id, statu_id,
                d["Statutory_Applicable_Status"],
                d["Statutory_remarks"], comp_id,
                d["Compliance_Applicable_Status"], submitted_status,
                approval_status, int(user_id), created_on,
                int(user_id), created_on
            ))

        if values:
            self._source_db.bulk_insert(
                "tbl_client_compliances", columns, values
            )
            return True
        else:
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
            "Secondary_Legislation": self.check_child_statutories,
            "Statutory_Provision": self.check_statutory_provision,
            "Compliance_Task": self.check_compliance_task,
            "Compliance_Description": self.check_compliance_description,
            "Organization": self.check_organisation,
            "Statutory_Applicable_Status": self.check_applicable_status,
            "Compliance_Applicable_Status": self.check_applicable_status
        }

    def csv_column_fields(self):
        self._csv_column_name = [
            "S.No", "Client_Group", "Legal_Entity", "Domain",
            "Organization", "Unit_Code", "Unit_Name",
            "Unit_Location", "Primary_Legislation", "Secondary_Legislation",
            "Statutory_Provision", "Compliance_Task",
            "Compliance_Description", "Statutory_Applicable_Status",
            "Statutory_remarks", "Compliance_Applicable_Status"
        ]

    def check_compliance_task_name_duplicate(
        self, domain_name, unit_code, statutory_provision, task_name,
        compliance_description
    ):
        data = self._db.call_proc("sp_check_duplicate_compliance_for_unit", [
            domain_name, unit_code, statutory_provision, task_name,
            compliance_description
        ])
        if len(data) > 0:
            return False
        else:
            return True

    def check_compliance_task_name_duplicate_in_knowledge(
        self, domain_name, unit_code, statutory_provision,
        task_name, compliance_description
    ):
        unit_id = self.Unit_Code.get(unit_code).get("unit_id")
        domain_id = self.Domain.get(domain_name).get("domain_id")
        c_ids = self._source_db.call_proc(
            "sp_bu_get_compliance_id_by_name",
            [task_name, compliance_description]
        )
        comp_id = c_ids[0]["compliance_id"]
        data = self._source_db.call_proc(
            "sp_bu_check_duplicate_compliance_for_unit",
            [domain_id, unit_id, comp_id]
        )
        if len(data) > 0:
            return False
        else:
            return True

    def save_executive_message(
        self, a_type, csv_name, clientgroup, legalentity, createdby, unitids
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
            action_type = "rejected"

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
        self.errorSummary()
        self._client_id = None
        self._client_group = None
        self._unit_ids = []
        self._legal_entity_id = None
        self._legal_entity = None
        self._domain_ids = []
        self._domain_names = []
        self._sheet_name = "Assign Statutory"

    # error summary mapped with initial count
    def errorSummary(self):
        self._error_summary = {
            "mandatory_error": 0,
            "max_length_error": 0,
            "duplicate_error": 0,
            "invalid_char_error": 0,
            "invalid_data_error": 0,
            "inactive_error": 0
        }

    def compare_csv_columns(self):
        res = collections.Counter(
            self._csv_column_name) == collections.Counter(self._csv_header)
        return res
    '''
        looped csv data to perform corresponding validation
        returns: valid and invalid return format
        rType: dictionary
    '''

    def check_duplicate_in_csv(self):
        seen = set()
        for d in self._source_data:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)

        if len(seen) != len(self._source_data):
            raise ValueError("Duplicate data found in CSV")

    def check_duplicate_compliance_for_same_unit_in_csv(self):
        # self._source_data.sort(key=lambda x: (
        #     x["Domain"], x["Unit_Code"], x["Statutory_Provision"],
        #     x["Compliance_Task"], x["Compliance_Description"]
        # ))
        duplicate_compliance = 0
        duplicate_compliance_row = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"], s["Unit_Code"], s["Statutory_Provision"],
            s["Compliance_Task"], s["Compliance_Description"]
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

    def check_uploaded_count_in_csv(self):
        # self._source_data.sort(key=lambda x: (
        #     x["Domain"], x["Unit_Code"]
        # ))
        unit_names = []

        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"], s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                unit_code = grouped_list[0].get("Unit_Code")
                domain = grouped_list[0].get("Domain")
                unit_names.append(grouped_list[0].get("Unit_Code"))
                data = self._db.call_proc(
                    "sp_check_upload_compliance_count_for_unit",
                    [domain, unit_code]
                )
                uploaded_count = data[0]["count"]

                if(len(grouped_list) != uploaded_count):
                    error_msg = "Downloaded records and uploaded records are not same for unit %s" % (
                        ','.join(unit_names)
                    )
                    raise ValueError(str(error_msg))

    def get_master_table_info(self):
        # self._source_data.sort(key=lambda x: (
        #     x["Domain"], x["Unit_Code"]
        # ))
        self._domain_names = []
        self._domain_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Domain"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                self._domain_names.append(grouped_list[0].get("Domain"))

                if(
                    self.Domain.get(grouped_list[0].get("Domain"))
                ) != None:
                    self._domain_ids.append(self.Domain.get(
                        grouped_list[0].get("Domain")).get("domain_id")
                    )

                self._legal_entity = grouped_list[0].get("Legal_Entity")

                if(
                    self.Legal_Entity.get(grouped_list[0].get("Legal_Entity"))
                ) != None:
                    self._legal_entity_id = self.Legal_Entity.get(
                            grouped_list[0].get("Legal_Entity")
                        ).get("legal_entity_id")

                self._client_group = grouped_list[0].get("Client_Group")

                if(
                    self.Client_Group.get(grouped_list[0].get("Client_Group"))
                ) != None:
                    self._client_id = self.Client_Group.get(
                        grouped_list[0].get("Client_Group")
                        ).get("client_id")

        self._unit_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                if(
                    self.Unit_Code.get(grouped_list[0].get("Unit_Code"))
                ) != None:
                    self._unit_ids.append(self.Unit_Code.get(
                        grouped_list[0].get("Unit_Code")).get("unit_id")
                    )

    def check_invalid_compliance_in_csv(self, data):
        client_group = data.get("Client_Group")
        legal_entity = data.get("Legal_Entity")
        domain = data.get("Domain")
        organization = data.get("Organization").replace(CSV_DELIMITER, ",")
        unit_code = data.get("Unit_Code")
        unit_name = data.get("Unit_Name")
        unit_location = data.get("Unit_Location")
        primary_legislation = data.get("Primary_Legislation")
        secondary_legislation = data.get("Secondary_Legislation")
        statutory_provision = data.get("Statutory_Provision")
        compliance_task = data.get("Compliance_Task")
        compliance_description = data.get("Compliance_Description")

        res = self._db.call_proc(
            "sp_check_invalid_compliance_in_csv",
            [
                client_group, legal_entity, domain, organization, unit_code,
                unit_name, unit_location, primary_legislation,
                secondary_legislation, statutory_provision, compliance_task,
                compliance_description
            ]
        )
        if len(res) > 0:
            return True
        else:
            return False

    def perform_validation(self):
        mapped_error_dict = {}
        mapped_header_dict = {}
        invalid = 0
        # self.check_duplicate_in_csv()
        duplicate = self.check_duplicate_compliance_for_same_unit_in_csv()
        duplicate_compliance_in_csv = duplicate[0]
        duplicate_compliance_row = duplicate[1]
        self._error_summary["duplicate_error"] += duplicate_compliance_in_csv

        self.init_values(self._session_user_obj.user_id())

        def make_error_desc(res, msg):
            if res is True:
                res = []
            if res is not True:
                if type(msg) is list:
                    res.extend(msg)
                else:
                    res.append(msg)
            return res

        # res = True
        # dup_error = "Compliance_Task - Duplicate data"
        # res = make_error_desc(res, dup_error)

        for row_idx, data in enumerate(self._source_data):
            res = True
            error_count = {"mandatory": 0, "max_length": 0, "invalid_char": 0}
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
                                ) == 'Not Applicable' or
                                data.get(
                                    'Statutory_Applicable_Status'
                                ) == 'Do not Show'
                            ) and
                            data.get(
                                'Statutory_remarks'
                            ) == ''
                        )
                    ):
                        self._error_summary["mandatory_error"] += 1
                        mandatory_error = "Statutory_remarks - Field is blank"
                        res = make_error_desc(res, mandatory_error)

                    if (
                        key == 'Statutory_remarks' and
                        (
                            data.get(
                                'Statutory_Applicable_Status'
                            ) == 'Applicable' and
                            data.get(
                                'Statutory_remarks'
                            ) != ''
                        )
                    ):
                        self._error_summary["mandatory_error"] += 1
                        mandatory_error = "Statutory_Remarks - Not Required"
                        res = make_error_desc(res, mandatory_error)

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
                            error_count["max_length"] += error_cnt[
                                "max_length"
                            ]
                            error_count["invalid_char"] += error_cnt[
                                "invalid_char"
                            ]
                    if v != "":
                        if (
                            csvParam.get("check_is_exists") is True or
                            csvParam.get("check_is_active") is True
                        ):
                            unboundMethod = self._validation_method_maps.get(
                                key
                            )
                            if unboundMethod is not None:
                                isFound = unboundMethod(v)

                            if isFound is not True and isFound != "":
                                msg = "%s - %s" % (key, isFound)
                                if res is not True:
                                    res.append(msg)
                                else:
                                    res = [msg]
                                if "Status" in isFound:
                                    self._error_summary[
                                        "inactive_error"
                                    ] += 1
                                else:
                                    self._error_summary[
                                        "invalid_data_error"
                                    ] += 1

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
                            dup_error = "Compliance_Task_Name - Duplicate Compliances in CSV"
                            res = make_error_desc(res, dup_error)

            if res is not True:
                error_list = mapped_error_dict.get(row_idx)
                if error_list is None:
                    error_list = res
                else:
                    error_list.extend(res)
                res = True

                mapped_error_dict[row_idx] = error_list

                # head_idx = mapped_header_dict.get(key)
                # if head_idx is None:
                #     head_idx = [row_idx]
                # else:
                #     head_idx.append(row_idx)

                # mapped_header_dict[key] = head_idx
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

        if invalid == 0:
            self.check_uploaded_count_in_csv()
            for row_idx, data in enumerate(self._source_data):
                res = True

                if not self.check_compliance_task_name_duplicate(
                    data.get("Domain"), data.get("Unit_Code"),
                    data.get("Statutory_Provision"), data.get(
                        "Compliance_Task"
                    ),
                    data.get("Compliance_Description"),
                ):
                    self._error_summary["duplicate_error"] += 1
                    dup_error = "Compliance_Task_Name - Duplicate Compliances in Temp DB"
                    res = make_error_desc(res, dup_error)

                if not self.check_compliance_task_name_duplicate_in_knowledge(
                    data.get("Domain"), data.get("Unit_Code"),
                    data.get("Statutory_Provision"),
                    data.get("Compliance_Task"),
                    data.get("Compliance_Description"),
                ):
                    self._error_summary["duplicate_error"] += 1
                    dup_error = "Compliance_Task_Name - Duplicate Compliances in Knowledge"
                    res = make_error_desc(res, dup_error)

                if not self.check_invalid_compliance_in_csv(
                    data
                ):
                    self._error_summary["invalid_data_error"] += 1
                    invalid_error = "Invalid Compliance to this Unit"
                    res = make_error_desc(res, invalid_error)

                if res is not True:
                    error_list = mapped_error_dict.get(row_idx)
                    if error_list is None:
                        error_list = res
                    else:
                        error_list.extend(res)
                    res = True

                    mapped_error_dict[row_idx] = error_list

                    # head_idx = mapped_header_dict.get(key)
                    # if head_idx is None:
                    #     head_idx = [row_idx]
                    # else:
                    #     head_idx.append(row_idx)

                    # mapped_header_dict[key] = head_idx
                    invalid += 1

            self.get_master_table_info()

        if invalid > 0:
            return self.make_invalid_return(
                mapped_error_dict, mapped_header_dict
            )
        else:
            return self.make_valid_return(
                mapped_error_dict, mapped_header_dict
            )

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
        self._legal_entity = None
        self._client_group = None
        self._csv_name = None
        self._unit_ids = None

    def get_source_data(self):
        self._source_data = self._db.call_proc(
            "sp_assign_statutory_by_csvid", [self._csv_id]
        )

    def perform_validation_before_submit(self):
        declined_count = 0
        self._declined_row_idx = []
        self.init_values(self._session_user_obj.user_id())

        self._unit_ids = []
        for k, v in groupby(self._source_data, key=lambda s: (
            s["Unit_Code"]
        )):
            grouped_list = list(v)
            if len(grouped_list) > 1:
                if(
                    self.Unit_Code.get(grouped_list[0].get("Unit_Code"))
                ) != None:
                    self._unit_ids.append(self.Unit_Code.get(
                        grouped_list[0].get("Unit_Code")).get("unit_id")
                    )

        for row_idx, data in enumerate(self._source_data):
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
                                unboundMethod = self._validation_method_maps.get(
                                    key
                                )
                                if unboundMethod is not None:
                                    isFound = unboundMethod(v)

                            if isFound is not True and isFound != "":
                                declined_count += 1
                                print key, v

            if not self.check_compliance_task_name_duplicate_in_knowledge(
                data.get("Domain"), data.get("Unit_Code"),
                data.get("Statutory_Provision"), data.get("Compliance_Task"),
                data.get("Compliance_Description"),
            ):
                declined_count += 1

            if declined_count > 0:
                self._declined_row_idx.append(
                    data.get("bulk_assign_statutory_id")
                )
        return self._declined_row_idx

    def frame_data_for_main_db_insert(self, user_id):
        self.get_source_data()
        self._source_data.sort(key=lambda x: (
             x["Domain"], x["Unit_Name"]
        ))
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

            cs_id = self.save_client_statutories_data(
                self._client_id, unit_id, domain_id, user_id
                )
            self.save_client_compliances_data(
                self._client_id, self._legal_entity_id, unit_id, domain_id,
                cs_id, grouped_list, user_id
                )

    def make_rejection(self, declined_info, user_id):
        try:
            created_on = get_date_time()
            q = "update tbl_bulk_assign_statutory set " + \
                " action = 3 where bulk_assign_statutory_id in (%s)" % (
                    ",".join(map(str, declined_info))
                )
            self._db.execute(q)

            q1 = "update tbl_bulk_assign_statutory_csv set " + \
                " declined_count = %s, approve_status = 1, " + \
                " approved_by = %s, approved_on = %s where " + \
                " csv_assign_statutory_id = %s"
            self._db.execute(q1, [
                len(declined_info), user_id, created_on, self._csv_id
            ])

        except Exception, e:
            raise (e)
